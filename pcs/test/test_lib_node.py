from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import sys

from pcs.test.tools.pcs_unittest import TestCase, skipUnless

#python 2.6 does not support sys.version_info.major
need_python3 = skipUnless(sys.version_info[0] == 3, "test requires python3")
need_python2 = skipUnless(sys.version_info[0] == 2, "test requires python2")

import pcs.lib.node as lib

class NodeAddressesTest(TestCase):
    def test_properties_all(self):
        ring0 = "test_ring0"
        ring1 = "test_ring1"
        name = "test_name"
        id = "test_id"
        node = lib.NodeAddresses(ring0, ring1, name, id)
        self.assertEqual(ring0, node.ring0)
        self.assertEqual(ring1, node.ring1)
        self.assertEqual(name, node.label)
        self.assertEqual(id, node.id)

    def test_properties_required(self):
        ring0 = "test_ring0"
        node = lib.NodeAddresses(ring0)
        self.assertEqual(ring0, node.ring0)
        self.assertEqual(None, node.ring1)
        self.assertEqual(ring0, node.label)
        self.assertEqual(None, node.id)

    def test_hash(self):
        node0 = lib.NodeAddresses("node0")
        another_node0 = lib.NodeAddresses("node0")
        node1 = lib.NodeAddresses("node1")
        self.assertEqual(hash(node0), hash(another_node0))
        self.assertEqual(hash(node1), hash(node1))
        self.assertNotEqual(hash(node0), hash(node1))

    def test_equal(self):
        node0 = lib.NodeAddresses("node0")
        another_node0 = lib.NodeAddresses("node0")
        node1 = lib.NodeAddresses("node1")
        self.assertTrue(node0 == another_node0)
        self.assertTrue(another_node0 == node0)
        self.assertTrue(node1 == node1)
        self.assertFalse(node1 == node0)
        self.assertFalse(node0 == node1)

    def test_not_equal(self):
        node0 = lib.NodeAddresses("node0")
        another_node0 = lib.NodeAddresses("node0")
        node1 = lib.NodeAddresses("node1")
        self.assertFalse(node0 != another_node0)
        self.assertFalse(another_node0 != node0)
        self.assertFalse(node1 != node1)
        self.assertTrue(node0 != node1)
        self.assertTrue(node1 != node0)

    def test_less_than(self):
        node0 = lib.NodeAddresses("node0")
        another_node0 = lib.NodeAddresses("node0")
        node1 = lib.NodeAddresses("node1")
        self.assertFalse(node0 < another_node0)
        self.assertFalse(another_node0 < node0)
        self.assertFalse(node1 < node1)
        self.assertTrue(node0 < node1)
        self.assertFalse(node1 < node0)

@need_python3
class NodeAddressesRepr(TestCase):
    def test_host_only_specified(self):
        self.assertEqual(repr(lib.NodeAddresses("node0")), str(
            "<pcs.lib.node.NodeAddresses ['node0'], {'name': None, 'id': None}>"
        ))

    def test_host_and_name_specified(self):
        self.assertEqual(repr(lib.NodeAddresses("node0", name="name0")), str(
            "<pcs.lib.node.NodeAddresses ['node0'],"
            " {'name': 'name0', 'id': None}>"
        ))

    def test_host_name_and_id_specified(self):
        self.assertEqual(
            repr(lib.NodeAddresses("node0", name="name0", id="id0")),
            str(
                "<pcs.lib.node.NodeAddresses ['node0'],"
                " {'name': 'name0', 'id': 'id0'}>"
            )
        )

    def test_host_ring1_name_and_id_specified(self):
        self.assertEqual(
            repr(lib.NodeAddresses("node0", "node0-1", name="name0", id="id0")),
            str(
                "<pcs.lib.node.NodeAddresses ['node0', 'node0-1'],"
                " {'name': 'name0', 'id': 'id0'}>"
            )
        )

@need_python2
class NodeAddressesRepr_python2(TestCase):
    def test_host_only_specified(self):
        self.assertEqual(repr(lib.NodeAddresses("node0")), str(
            "<pcs.lib.node.NodeAddresses [u'node0'], {'name': None, 'id': None}>"
        ))

    def test_host_and_name_specified(self):
        self.assertEqual(repr(lib.NodeAddresses("node0", name="name0")), str(
            "<pcs.lib.node.NodeAddresses [u'node0'],"
            " {'name': u'name0', 'id': None}>"
        ))

    def test_host_name_and_id_specified(self):
        self.assertEqual(
            repr(lib.NodeAddresses("node0", name="name0", id="id0")),
            str(
                "<pcs.lib.node.NodeAddresses [u'node0'],"
                " {'name': u'name0', 'id': u'id0'}>"
            )
        )

    def test_host_ring1_name_and_id_specified(self):
        self.assertEqual(
            repr(lib.NodeAddresses("node0", "node0-1", name="name0", id="id0")),
            str(
                "<pcs.lib.node.NodeAddresses [u'node0', u'node0-1'],"
                " {'name': u'name0', 'id': u'id0'}>"
            )
        )


class NodeAddressesListTest(TestCase):
    def test_empty(self):
        nodes = lib.NodeAddressesList()
        self.assertEqual(0, len(nodes))
        self.assertEqual([], list(nodes))
        self.assertRaises(IndexError, lambda: nodes[0])

    def test_append(self):
        node1 = lib.NodeAddresses("node1")
        node2 = lib.NodeAddresses("node2")
        nodes = lib.NodeAddressesList()

        nodes.append(node1)
        self.assertEqual(1, len(nodes))
        self.assertEqual([node1], list(nodes))
        self.assertEqual(node1, nodes[0])

        nodes.append(node2)
        self.assertEqual(2, len(nodes))
        self.assertEqual([node1, node2], list(nodes))
        self.assertEqual(node1, nodes[0])
        self.assertEqual(node2, nodes[1])

    def test_create_from_empty_list(self):
        nodes = lib.NodeAddressesList([])
        self.assertEqual(0, len(nodes))
        self.assertEqual([], list(nodes))
        self.assertRaises(IndexError, lambda: nodes[0])

    def test_create_from_list(self):
        node1 = lib.NodeAddresses("node1")
        node2 = lib.NodeAddresses("node2")
        nodes = lib.NodeAddressesList([node1, node2])
        self.assertEqual(2, len(nodes))
        self.assertEqual([node1, node2], list(nodes))
        self.assertEqual(node1, nodes[0])
        self.assertEqual(node2, nodes[1])

    def test_create_from_node_list(self):
        node1 = lib.NodeAddresses("node1")
        node2 = lib.NodeAddresses("node2")
        node3 = lib.NodeAddresses("node3")
        nodes_source = lib.NodeAddressesList([node1, node2])
        nodes = lib.NodeAddressesList(nodes_source)
        nodes_source.append(node3)

        self.assertEqual(2, len(nodes))
        self.assertEqual([node1, node2], list(nodes))
        self.assertEqual(node1, nodes[0])
        self.assertEqual(node2, nodes[1])

    def test_find_by_label(self):
        node0 = lib.NodeAddresses("node0")
        node1 = lib.NodeAddresses("node1")
        node_list = lib.NodeAddressesList([node0, node1])
        self.assertEqual(node1, node_list.find_by_label("node1"))
        self.assertEqual(node0, node_list.find_by_label("node0"))
        self.assertRaises(
            lib.NodeNotFound, lambda: node_list.find_by_label("node2")
        )

class NodeAddressesList__add__(TestCase):
    def test_can_add_node_addresses_list(self):
        node0 = lib.NodeAddresses("node0")
        node1 = lib.NodeAddresses("node1")
        node2 = lib.NodeAddresses("node2")
        self.assertEqual(lib.NodeAddressesList(
            [node0, node1, node2])._list,
            (
                lib.NodeAddressesList([node0, node1])
                +
                lib.NodeAddressesList([node2])
            )._list
        )

    def test_can_add_list(self):
        node0 = lib.NodeAddresses("node0")
        node1 = lib.NodeAddresses("node1")
        node2 = lib.NodeAddresses("node2")
        self.assertEqual(lib.NodeAddressesList(
            [node0, node1, node2])._list,
            (
                lib.NodeAddressesList([node0, node1])
                +
                [node2]
            )._list
        )
