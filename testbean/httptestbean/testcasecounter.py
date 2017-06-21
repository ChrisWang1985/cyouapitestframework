# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""


class TestCaseCounter(object):
    def __init__(self):
        self._start_time = None
        self._end_time = None
        self._duration_time = None
        self._result_object = {}
        self._test_case = None
        self._error_count = 0
        self._pass_count = 0
        self._fail_count = 0

    def set_start_time(self, start_time):
        self._start_time = start_time

    def get_start_time(self):
        return self._start_time

    def set_end_time(self, end_time):
        self._end_time = end_time

    def get_end_time(self):
        return self._end_time

    def get_duration_time(self):
        self._duration_time = self._end_time - self._start_time

        return self._duration_time

    def set_result_object(self, result, running_message):
        self._result_object = {"result": result, "msg": running_message}

    def get_result_object(self):
        return self._result_object

    def get_result_object_with_key(self, key):
        if key in self._result_object.keys():
            return self._result_object[key]
        else:
            return ""

    def set_test_case(self, test_case):
        self._test_case = test_case

    def get_test_case(self):
        return self._test_case