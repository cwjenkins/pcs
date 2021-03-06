from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from pcs.test.tools.pcs_unittest import TestCase

from pcs.common import report_codes
from pcs.lib.booth import env
from pcs.lib.errors import ReportItemSeverity as severities
from pcs.test.tools.assertions import assert_raise_library_error
from pcs.test.tools.misc import create_patcher
from pcs.test.tools.pcs_unittest import mock

patch_env = create_patcher("pcs.lib.booth.env")

class GetConfigFileNameTest(TestCase):
    @patch_env("os.path.exists")
    def test_refuse_when_name_starts_with_slash(self, mock_path_exists):
        mock_path_exists.return_value = True
        assert_raise_library_error(
            lambda: env.get_config_file_name("/booth"),
            (
                severities.ERROR,
                report_codes.BOOTH_INVALID_NAME,
                {
                    "name": "/booth",
                    "reason": "contains illegal character '/'",
                }
            ),
        )

class BoothEnvTest(TestCase):
    @patch_env("RealFile")
    def test_get_content_from_file(self, mock_real_file):
        mock_real_file.return_value = mock.MagicMock(
            read=mock.MagicMock(return_value="content")
        )
        self.assertEqual(
            "content",
            env.BoothEnv("report processor", env_data={"name": "booth"})
                .get_config_content()
        )

    @patch_env("set_keyfile_access")
    @patch_env("RealFile")
    def test_create_config(self, mock_real_file, mock_set_keyfile_access):
        mock_file = mock.MagicMock(
            assert_no_conflict_with_existing=mock.MagicMock(),
            write=mock.MagicMock(),
        )
        mock_real_file.return_value = mock_file


        env.BoothEnv(
            "report processor",
            env_data={"name": "booth"}
        ).create_config("a", can_overwrite_existing=True)

        self.assertEqual(mock_file.assert_no_conflict_with_existing.mock_calls,[
            mock.call('report processor', True),
        ])
        self.assertEqual(mock_file.write.mock_calls, [mock.call('a')])

    @patch_env("RealFile")
    def test_push_config(self, mock_real_file):
        mock_file = mock.MagicMock(
            assert_no_conflict_with_existing=mock.MagicMock(),
            write=mock.MagicMock(),
        )
        mock_real_file.return_value = mock_file
        env.BoothEnv(
            "report processor",
            env_data={"name": "booth"}
        ).push_config("a")
        mock_file.write.assert_called_once_with("a")



    def test_export_config_file_when_was_present_in_env_data(self):
        self.assertEqual(
            env.BoothEnv(
                "report processor",
                {
                    "name": "booth-name",
                    "config_file": {
                        "content": "a\nb",
                    },
                    "key_file": {
                        "content": "secure",
                    },
                    "key_path": "/path/to/file.key",
                }
            ).export(),
            {
                "config_file": {
                    "content": "a\nb",
                    "can_overwrite_existing_file": False,
                    "no_existing_file_expected": False,
                    "is_binary": False,
                },
                "key_file": {
                    "content": "secure",
                    "can_overwrite_existing_file": False,
                    "no_existing_file_expected": False,
                    "is_binary": True,
                },
            }
        )

    def test_do_not_export_config_file_when_no_provided(self):
        self.assertEqual(
            env.BoothEnv("report processor", {"name": "booth"}).export(),
            {}
        )

class SetKeyfileAccessTest(TestCase):
    @patch_env("os.chmod")
    @patch_env("os.chown")
    @patch_env("grp.getgrnam")
    @patch_env("pwd.getpwnam")
    @patch_env("settings")
    def test_do_everything_to_set_desired_file_access(
        self, settings, getpwnam, getgrnam, chown, chmod
    ):
        file_path = "/tmp/some_booth_file"
        env.set_keyfile_access(file_path)

        getpwnam.assert_called_once_with(settings.pacemaker_uname)
        getgrnam.assert_called_once_with(settings.pacemaker_gname)

        chown.assert_called_once_with(
            file_path,
            getpwnam.return_value.pw_uid,
            getgrnam.return_value.gr_gid,
        )

    @patch_env("pwd.getpwnam", mock.MagicMock(side_effect=KeyError))
    @patch_env("settings.pacemaker_uname", "some-user")
    def test_raises_when_cannot_get_uid(self):
        assert_raise_library_error(
            lambda: env.set_keyfile_access("/booth"),
            (
                severities.ERROR,
                report_codes.UNABLE_TO_DETERMINE_USER_UID,
                {
                    "user": "some-user",
                }
            ),
        )

    @patch_env("grp.getgrnam", mock.MagicMock(side_effect=KeyError))
    @patch_env("pwd.getpwnam", mock.MagicMock())
    @patch_env("settings.pacemaker_gname", "some-group")
    def test_raises_when_cannot_get_gid(self):
        assert_raise_library_error(
            lambda: env.set_keyfile_access("/booth"),
            (
                severities.ERROR,
                report_codes.UNABLE_TO_DETERMINE_GROUP_GID,
                {
                    "group": "some-group",
                }
            ),
        )

    @patch_env("format_environment_error", mock.Mock(return_value="err"))
    @patch_env("os.chown", mock.MagicMock(side_effect=EnvironmentError()))
    @patch_env("grp.getgrnam", mock.MagicMock())
    @patch_env("pwd.getpwnam", mock.MagicMock())
    @patch_env("settings.pacemaker_gname", "some-group")
    def test_raises_when_cannot_chown(self):
        assert_raise_library_error(
            lambda: env.set_keyfile_access("/booth"),
            (
                severities.ERROR,
                report_codes.FILE_IO_ERROR,
                {
                    'reason': 'err',
                    'file_role': u'BOOTH_KEY',
                    'file_path': '/booth',
                    'operation': u'chown',
                }
            ),
        )

    @patch_env("format_environment_error", mock.Mock(return_value="err"))
    @patch_env("os.chmod", mock.MagicMock(side_effect=EnvironmentError()))
    @patch_env("os.chown", mock.MagicMock())
    @patch_env("grp.getgrnam", mock.MagicMock())
    @patch_env("pwd.getpwnam", mock.MagicMock())
    @patch_env("settings.pacemaker_gname", "some-group")
    def test_raises_when_cannot_chmod(self):
        assert_raise_library_error(
            lambda: env.set_keyfile_access("/booth"),
            (
                severities.ERROR,
                report_codes.FILE_IO_ERROR,
                {
                    'reason': 'err',
                    'file_role': u'BOOTH_KEY',
                    'file_path': '/booth',
                    'operation': u'chmod',
                }
            ),
        )
