# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

from testcaseinfocounter import TestCaseInfoCounter
from testcasecounter import TestCaseCounter
import datetime

class TestSuiteCounter(object):
    def __init__(self):
        self._test_case_info_counter_list = []

    def append_test_case_info_counter(self, test_case_info_counter):
        self._test_case_info_counter_list.append(test_case_info_counter)

    def get_test_case_info_counter(self):
        return self._test_case_info_counter_list

    def get_test_info_length(self):
        return len(self._test_case_info_counter_list)

    def get_pass_count(self):
        _pass_count = 0

        for i in range(len(self._test_case_info_counter_list)):
            _info_count = self._test_case_info_counter_list[i]
            _pass_count += _info_count.get_pass_count()

        return _pass_count

    def get_fail_count(self):
        _fail_count = 0

        for i in range(len(self._test_case_info_counter_list)):
            _info_count = self._test_case_info_counter_list[i]
            _fail_count += _info_count.get_fail_count()

        return _fail_count

    def get_error_count(self):
        _error_count = 0

        for i in range(len(self._test_case_info_counter_list)):
            _info_count = self._test_case_info_counter_list[i]
            _error_count += _info_count.get_error_count()

        return _error_count

    def get_skip_count(self):
        _skip_count = 0

        for i in range(len(self._test_case_info_counter_list)):
            _info_count = self._test_case_info_counter_list[i]
            _skip_count += _info_count.get_skip_count()

        return _skip_count


if __name__ == '__main__':
    test_suite_counter = TestSuiteCounter()
    bvt_test_case_info_counter = TestCaseInfoCounter()
    fvt_test_case_info_counter = TestCaseInfoCounter()

    bvt_test_case_info_counter.set_start_time(datetime.datetime.now())

    for i in range(25):
        bvt_test_case_counter = TestCaseCounter()
        bvt_test_case_counter.set_start_time(datetime.datetime.now())

        if (i % 7) == 0:
            bvt_test_case_counter.set_result_object("fail", "BVT test case failure!")
        else:
            bvt_test_case_counter.set_result_object("pass", "BVT test case pass!")

        bvt_test_case_counter.set_end_time(datetime.datetime.now())
        bvt_test_case_info_counter.append_test_case_counter(bvt_test_case_counter)

    bvt_test_case_info_counter.set_end_time(datetime.datetime.now())

    fvt_test_case_info_counter.set_start_time(datetime.datetime.now())

    for i in range(75):
        fvt_test_case_counter = TestCaseCounter()
        fvt_test_case_counter.set_start_time(datetime.datetime.now())

        if (i % 9) == 0:
            fvt_test_case_counter.set_result_object("fail", "FVT test case failure!")
        else:
            fvt_test_case_counter.set_result_object("pass", "FVT test case pass!")

        fvt_test_case_counter.set_end_time(datetime.datetime.now())
        fvt_test_case_info_counter.append_test_case_counter(fvt_test_case_counter)

    fvt_test_case_info_counter.set_end_time(datetime.datetime.now())

    test_suite_counter.append_test_case_info_counter(bvt_test_case_info_counter)
    test_suite_counter.append_test_case_info_counter(fvt_test_case_info_counter)

    print test_suite_counter.get_pass_count()
    print test_suite_counter.get_fail_count()
