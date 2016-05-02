from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from pcs.lib.errors import ReportItem
from pcs.lib import error_codes

def value_out_of_set(set_type, allowed_values, value):
    return ReportItem.error(
        error_codes.VALUE_OUT_OF_SET,
        "invalid {set_type} '{value}', allowed values are: {allowed_values}",
        info={
            'set_type': set_type,
            'value': value,
            'allowed_values_raw': allowed_values,
            'allowed_values': ", ".join(allowed_values)
        },
    )

def required_option_is_missing(name):
    return ReportItem.error(
        error_codes.REQUIRED_OPTION_IS_MISSING,
        "required attribute '{name}' is missing",
        info={
            "name": name
        },
    )

def resource_is_in_master(resource_id, master_id):
    return ReportItem.error(
        error_codes.RESOURCE_IS_IN_MASTER,
        "{resource_id} is a master/slave resource, you should use the"
            +" master id: {master_id} when adding constraints."
            +" Use --force to override."
        ,
        info={
            'resource_id': resource_id,
            'master_id': master_id
        },
    )

def resource_is_in_clone(resource_id, clone_id):
    return ReportItem.error(
        error_codes.RESOURCE_IS_IN_CLONE,
        "{resource_id} is a clone resource, you should use the"
            +" clone id: {clone_id} when adding constraints."
            +" Use --force to override."
        ,
        info={
            'resource_id': resource_id,
            'clone_id': clone_id
        },
    )

def resource_does_not_exist(resource_id):
    return ReportItem.error(
        error_codes.RESOURCE_DOES_NOT_EXIST,
        "Resource '{resource_id}' does not exist",
        info={
            'resource_id': resource_id,
        },
    )

def invalid_option(allowed_options, option_name):
    return ReportItem.error(
        error_codes.INVALID_OPTION,
        "invalid option '{option}', allowed options are: {allowed}",
        info={
            'option': option_name,
            'allowed_raw': sorted(allowed_options),
            'allowed': ", ".join(sorted(allowed_options))
        },
    )

def invalid_option_value(allowed_values, option_name, option_value):
    return ReportItem.error(
        error_codes.INVALID_OPTION_VALUE,
        "invalid value '{option_value}' of option '{option_name}',"
            +" allowed values are: {allowed_values}",
        info={
            'option_value': option_value,
            'option_name': option_name,
            'allowed_values_raw': allowed_values,
            'allowed_values': ", ".join(allowed_values)
        },
    )

def duplicit_constraints_exist(type, constraint_info_list):
    return ReportItem.error(
        error_codes.DUPLICIT_CONSTRAINTS_EXIST,
        "duplicate constraint already exists",
        forceable=True,
        info={
            'type': type,
            'constraint_info_list': constraint_info_list,
        },
    )

def multiple_score_options():
    return ReportItem.error(
        error_codes.MULTIPLE_SCORE_OPTIONS,
        "you cannot specify multiple score options",
    )

def invalid_score(score):
    return ReportItem.error(
        error_codes.INVALID_SCORE,
        "invalid score '{score}', use integer or INFINITY or -INFINITY",
        info={
            "score": score,
        }
    )
