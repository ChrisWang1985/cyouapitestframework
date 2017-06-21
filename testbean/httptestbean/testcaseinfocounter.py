# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

import datetime
from testcasecounter import TestCaseCounter


class TestCaseInfoCounter(object):
    def __init__(self):
        self._start_time = None
        self._end_time = None
        self._test_case_counter_list = []
        self._result_object = {}
        self._api_http_url = ""
        self._api_http_method = ""
        self._api_desc = ""
        self._pass_count = 0
        self._fail_count = 0
        self._error_count = 0
        self._skip_count = 0

    def set_start_time(self, start_time):
        self._start_time = start_time

    def get_start_time(self):
        return self._start_time

    def set_end_time(self, end_time):
        self._end_time = end_time

    def get_end_time(self):
        return self._end_time

    def get_duration_time(self):
        return self._end_time - self._start_time

    def append_test_case_counter(self, test_case_counter):
        _status = test_case_counter.get_result_object_with_key("result")

        if _status.lower() == "pass":
            self._pass_count += 1
        elif _status.lower() == "fail":
            self._fail_count += 1
        elif _status.lower() == "error":
            self._error_count += 1
        else:
            self._skip_count += 1

        self._test_case_counter_list.append(test_case_counter)

    def get_test_case_counter_list(self):
        return self._test_case_counter_list

    def get_test_case_counter_length(self):
        return len(self._test_case_counter_list)

    def get_result_object(self):
        _result = True
        _result_message = "%d test pass, %d test failure, %d test error, %d test skip. Pass rate is %d%%" % \
                          (self._pass_count, self._fail_count, self._error_count, self._skip_count,
                           (float(self._pass_count) / float(self.get_test_case_counter_length())) * 100)

        if self._error_count > 0 or self._fail_count > 0:
            _result = False

        self._result_object = {"result": _result, "msg": _result_message}

        return self._result_object

    def set_api_http_url(self, url):
        self._api_http_url = url

    def get_api_http_url(self):
        return self._api_http_url

    def set_api_http_method(self, method):
        self._api_http_method = method

    def get_api_http_method(self):
        return self._api_http_method

    def set_api_desc(self, desc):
        self._api_desc = desc

    def get_api_desc(self):
        return self._api_desc

    def get_pass_count(self):
        return self._pass_count

    def get_fail_count(self):
        return self._fail_count

    def get_error_count(self):
        return self._error_count

    def get_skip_count(self):
        return self._skip_count


if __name__ == '__main__':
    test_case_info_counter = TestCaseInfoCounter()
    test_case_info_counter.set_api_http_url('http://ip.taobao.com/restfulapi')
    test_case_info_counter.set_api_http_method('get')
    test_case_info_counter.set_api_desc('Get ip details')
    test_case_info_counter.set_start_time(datetime.datetime.now())

    for i in range(75):
        test_case__result_counter = TestCaseCounter()
        test_case__result_counter.set_start_time(datetime.datetime.now())

        if (i % 5) == 0:
            test_case__result_counter.set_result_object("fail", "Test case failure!")
        elif (i % 8) == 0:
            test_case__result_counter.set_result_object("error", "Test case error!")
        else:
            test_case__result_counter.set_result_object("pass", "Test case pass!")

        test_case__result_counter.set_end_time(datetime.datetime.now())
        test_case_info_counter.append_test_case_counter(test_case__result_counter)

    print test_case_info_counter.get_result_object()

    test_case_info_counter.set_end_time(datetime.datetime.now())