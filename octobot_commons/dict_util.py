#  Drakkar-Software OctoBot-Commons
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.


def find_nested_value(dict_, field):
    """
    Find a nested value in a dict
    :param dict_: the dict
    :param field: the field to search
    :return: a tuple : True if found else False, the dict at field value else the field
    """
    if field in dict_:
        return True, dict_[field]
    for value in dict_.values():
        if isinstance(value, dict):
            found_value, possible_value = find_nested_value(value, field)
            if found_value:
                return found_value, possible_value
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    found_value, possible_value = find_nested_value(item, field)
                    if found_value:
                        return found_value, possible_value
    return False, field


def check_and_merge_values_from_reference(
    current_dict, reference_dict, exception_list, logger=None
):
    """
     Check and merge dicts
    :param current_dict: the dict to be merged
    :param reference_dict: the reference dict
    :param exception_list: the merge exception list
    :param logger: the logger
    """
    for key, val in reference_dict.items():
        if key not in current_dict:
            current_dict[key] = val
            if logger is not None:
                logger.warning(
                    f"Missing {key} in configuration, added default value: {val}"
                )
        elif isinstance(val, dict) and key not in exception_list:
            check_and_merge_values_from_reference(
                current_dict[key], val, exception_list, logger=logger
            )
