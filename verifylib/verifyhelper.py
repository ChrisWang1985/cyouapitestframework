# -*- coding: utf-8 -*-
"""
    Http response verify helper library
    ~~~~~~~~~~~~~~

    Author: QATeam SDET-Chris Wang

    :copyright: (c) 2012 by CYou 17173.com.
"""
from jsonpath_rw import parse
import json
import re
from caseexceptions.assertexception import AssertException
from caseexceptions.assertfailException import AssertFailException


class HTTPVerifyHelper:
    def __init__(self):
        pass

    def _unicode_list_item(self, list_value):
        _list_length = len(list_value)
        _unicode_value_list = []

        for i in range(_list_length):
            _unicode_value_list.append(unicode(list_value[i]))

        return _unicode_value_list

    def verify_by_json_path(self, response_value, json_path, expect_value_list, is_case_sensitive=False):
        _json_obj = json.loads(response_value)

        _json_obj_expr = parse(json_path)
        _result_value_list = [match.value for match in _json_obj_expr.find(_json_obj)]
        _expect_value_list = expect_value_list

        _result_value_list = self._unicode_list_item(_result_value_list)
        _expect_value_list = self._unicode_list_item(_expect_value_list)

        if is_case_sensitive:
            _result_value_list = [value.lower() for value in _result_value_list]
            _expect_value_list = [unicode(value.lower()) for value in expect_value_list]

        return {"result": _result_value_list == _expect_value_list, "expect": _expect_value_list,
                "actual": _result_value_list}

    def verify_by_full_compare(self, response_value, expect_value_list):
        _sorted_result_value = sorted([repr(x) for x in response_value])
        _sorted_expect_value = sorted([repr(x) for x in expect_value_list])

        return {"result": _sorted_expect_value == _sorted_result_value, "expect": _sorted_expect_value,
                "actual": _sorted_result_value}

    def verify_by_reg_expression(self, response_value, regex_pattern, expect_value_list):
        _pattern = re.compile(regex_pattern)

        _sorted_result_value = sorted(_pattern.findall(response_value))
        _sorted_expect_value = sorted(expect_value_list)

        return {"result": _sorted_result_value == _sorted_expect_value, "expect": _sorted_expect_value,
                "actual": _sorted_result_value}

    def verify(self, response_value, assert_pattern_list, assert_value_list):
        _assert_pattern_list_length = len(assert_pattern_list)

        if _assert_pattern_list_length is 0:
            return

        _assert_mode = assert_pattern_list[0].lower()

        try:
            if _assert_mode == "jsonpath":
                if isinstance(assert_value_list, list):
                    _result = self.verify_by_json_path(response_value, assert_pattern_list[1], assert_value_list)
                else:
                    _result = self.verify_by_json_path(response_value, assert_pattern_list[1], assert_value_list)
            elif _assert_mode == "regex":
                if isinstance(assert_value_list, list):
                    _result = self.verify_by_reg_expression(response_value, assert_pattern_list[1], assert_value_list)
                else:
                    _result = self.verify_by_reg_expression(response_value, assert_pattern_list[1], assert_value_list)
            elif _assert_mode == "fullcompare":
                _result = self.verify_by_full_compare(response_value, assert_value_list)
            elif _assert_mode == "sql":
                pass
            else:
                raise Exception("Not supported assert pattern %s" % _assert_mode)
        except Exception, ex:
            raise AssertException(ex.message)

        if _result["result"]:
            return "pass"
        else:
            _error_message = "assert pattern is: " + _assert_mode + "<br>"
            _error_message += "except is " + ",".join(_result["expect"]) + "<br>"
            _error_message += "result is " + ",".join(_result["actual"]) + "<br>"
            raise AssertFailException(_error_message)