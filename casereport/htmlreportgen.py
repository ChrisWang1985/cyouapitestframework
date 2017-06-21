# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
from testbean.httptestbean.httptestcase import HTTPTestCase
from testbean.httptestbean.httptestcaseinfo import HTTPTestCaseInfo
from testbean.httptestbean.testcasecounter import TestCaseCounter
from testbean.httptestbean.testcaseinfocounter import TestCaseInfoCounter
from testbean.httptestbean.testsuitcounter import TestSuiteCounter
import datetime
import time


class HTMLReportGenerator(object):
    TABLE_START = "<table border=\"1\">"
    TABLE_END = "</table>"
    TR_START = "<tr>"
    TR_END = "</tr>"
    TD_START = "<td>"
    TD_END = "</td>"
    TD_Template_start = "<td %s>"

    def __init__(self, result_list):
        self.html_report_content = ""
        self._result_list = result_list

    def _generate_summary_table(self):
        # _api_case_length = self._result_list.get_test_info_length()
        _api_pass_count = self._result_list.get_pass_count()
        _api_fail_count = self._result_list.get_fail_count()
        _api_error_count = self._result_list.get_error_count()
        _api_skip_count = self._result_list.get_skip_count()
        _api_total_count = _api_pass_count + _api_fail_count + _api_error_count + _api_skip_count
        _api_pass_rate = float(_api_pass_count) / float(_api_total_count) * 100
        _api_fail_rate = float(_api_fail_count) / float(_api_total_count) * 100
        _api_error_rate = float(_api_error_count) / float(_api_total_count) * 100
        _api_skip_rate = float(_api_skip_count) / float(_api_total_count) * 100

        _summary_table_content = "<h2>Summary:</h2>"
        _summary_table_content += HTMLReportGenerator.TABLE_START

        _summary_table_content += HTMLReportGenerator.TR_START
        _summary_table_content += HTMLReportGenerator.TD_START + HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + "Pass" + HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + "Fail" + HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + "Error" + HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + "Skip" + HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + "Total" + HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TR_END

        _summary_table_content += HTMLReportGenerator.TR_START
        _summary_table_content += HTMLReportGenerator.TD_START + "Num:" + HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + str(_api_pass_count) + HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + str(_api_fail_count) + HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + str(_api_error_count) + HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + str(_api_skip_count) + HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + str(_api_total_count) + HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TR_END

        _summary_table_content += HTMLReportGenerator.TR_START
        _summary_table_content += HTMLReportGenerator.TD_START + "Rate:" + HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + str(_api_pass_rate)[:5] + "%" + \
            HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + str(_api_fail_rate)[:5] + "%" + \
            HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + str(_api_error_rate)[:5] + "%" + \
            HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + str(_api_skip_rate)[:5] + "%" + \
            HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TD_START + str(_api_pass_rate)[:5] + "%" + \
            HTMLReportGenerator.TD_END
        _summary_table_content += HTMLReportGenerator.TR_END

        _summary_table_content += HTMLReportGenerator.TABLE_END

        return _summary_table_content

    def _generate_details_table(self):
        _tb_details_content = "<h2>Details:</h2>"
        _tb_details_content += HTMLReportGenerator.TABLE_START
        _tb_details_content += HTMLReportGenerator.TR_START
        _tb_details_content += HTMLReportGenerator.TD_START + "URL" + HTMLReportGenerator.TD_END
        _tb_details_content += HTMLReportGenerator.TD_START + "Result" + HTMLReportGenerator.TD_END
        _tb_details_content += HTMLReportGenerator.TD_START + "Message" + HTMLReportGenerator.TD_END
        _tb_details_content += HTMLReportGenerator.TD_START + "DurationTime" + HTMLReportGenerator.TD_END
        _tb_details_content += HTMLReportGenerator.TD_START + "StartTime" + HTMLReportGenerator.TD_END
        _tb_details_content += HTMLReportGenerator.TD_START + "EndTime" + HTMLReportGenerator.TD_END
        _tb_details_content += HTMLReportGenerator.TD_START + "Method" + HTMLReportGenerator.TD_END
        _tb_details_content += HTMLReportGenerator.TD_START + "Description" + HTMLReportGenerator.TD_END
        _tb_details_content += HTMLReportGenerator.TR_END

        for ti_counter in self._result_list.get_test_case_info_counter():
            _tb_details_content += HTMLReportGenerator.TR_START
            _tb_details_content += HTMLReportGenerator.TD_Template_start % "width=\"150\"" \
                + ti_counter.get_api_http_url() + HTMLReportGenerator.TD_END
            _tb_details_content += HTMLReportGenerator.TD_Template_start % "width=\"100\"" \
                + str(ti_counter.get_result_object()["result"]) + HTMLReportGenerator.TD_END
            _tb_details_content += HTMLReportGenerator.TD_Template_start % "width=\"400\"" \
                + ti_counter.get_result_object()["msg"] + HTMLReportGenerator.TD_END
            _tb_details_content += HTMLReportGenerator.TD_Template_start % "width=\"120\"" \
                + str(ti_counter.get_duration_time()) + HTMLReportGenerator.TD_END
            _tb_details_content += HTMLReportGenerator.TD_Template_start % "width=\"230\"" \
                + str(ti_counter.get_start_time()) + HTMLReportGenerator.TD_END
            _tb_details_content += HTMLReportGenerator.TD_Template_start % "width=\"230\"" \
                + str(ti_counter.get_end_time()) + HTMLReportGenerator.TD_END
            _tb_details_content += HTMLReportGenerator.TD_Template_start % "width=\"100\"" \
                + ti_counter.get_api_http_method() + HTMLReportGenerator.TD_END
            _tb_details_content += HTMLReportGenerator.TD_Template_start % "width=\"300\"" \
                + ti_counter.get_api_desc() + HTMLReportGenerator.TD_END
            _tb_details_content += HTMLReportGenerator.TR_END

            _tb_details_content += HTMLReportGenerator.TR_START
            _tb_details_content += HTMLReportGenerator.TD_Template_start % "colspan=\"8\""
            _tb_details_content += self._generate_test_case_details_content(
                ti_counter.get_test_case_counter_list())
            _tb_details_content += HTMLReportGenerator.TD_END
            _tb_details_content += HTMLReportGenerator.TR_END

        _tb_details_content += HTMLReportGenerator.TABLE_END

        return _tb_details_content

    def _generate_test_case_details_content(self, test_case_counter_list):
        _tc_details_content = HTMLReportGenerator.TABLE_START

        _tc_details_content += HTMLReportGenerator.TR_START
        _tc_details_content += HTMLReportGenerator.TD_START + "CaseID" + HTMLReportGenerator.TD_END
        _tc_details_content += HTMLReportGenerator.TD_START + "Result" + HTMLReportGenerator.TD_END
        _tc_details_content += HTMLReportGenerator.TD_START + "Message" + HTMLReportGenerator.TD_END
        _tc_details_content += HTMLReportGenerator.TD_START + "DurationTime" + HTMLReportGenerator.TD_END
        _tc_details_content += HTMLReportGenerator.TD_START + "StartTime" + HTMLReportGenerator.TD_END
        _tc_details_content += HTMLReportGenerator.TD_START + "EndTime" + HTMLReportGenerator.TD_END
        _tc_details_content += HTMLReportGenerator.TD_START + "Description" + HTMLReportGenerator.TD_END
        _tc_details_content += HTMLReportGenerator.TR_END

        for tc_counter in test_case_counter_list:
            _tc_details_content += HTMLReportGenerator.TR_START
            _tc_details_content += HTMLReportGenerator.TD_Template_start % "width=\"145\"" \
                + str(tc_counter.get_test_case().get_case_id()) + HTMLReportGenerator.TD_END
            _tc_details_content += HTMLReportGenerator.TD_Template_start % "width=\"100\""\
                + str(tc_counter.get_result_object_with_key("result")) + HTMLReportGenerator.TD_END
            _tc_details_content += HTMLReportGenerator.TD_Template_start % "width=\"400\"" \
                + tc_counter.get_result_object_with_key("msg") + HTMLReportGenerator.TD_END
            _tc_details_content += HTMLReportGenerator.TD_Template_start % "width=\"120\"" \
                + str(tc_counter.get_duration_time()) + HTMLReportGenerator.TD_END
            _tc_details_content += HTMLReportGenerator.TD_Template_start % "width=\"230\"" \
                + str(tc_counter.get_start_time()) + HTMLReportGenerator.TD_END
            _tc_details_content += HTMLReportGenerator.TD_Template_start % "width=\"230\"" \
                + str(tc_counter.get_end_time()) + HTMLReportGenerator.TD_END
            _tc_details_content += HTMLReportGenerator.TD_Template_start % "width=\"400\"" \
                + tc_counter.get_test_case().get_case_desc() + HTMLReportGenerator.TD_END
            _tc_details_content += HTMLReportGenerator.TR_END

        _tc_details_content += HTMLReportGenerator.TABLE_END

        return _tc_details_content

    def get_report(self):
        return self._generate_summary_table() + "<br><br>" + self._generate_details_table()


def _mock_test_suite_counter_obj():
    suite = TestSuiteCounter()

    for i in range(3):
        test_case_info_object = HTTPTestCaseInfo("http://baidu.com/" + str(i), "", "get",
                                                 "获取参数" + str(i))
        _test_info_counter = TestCaseInfoCounter()
        _test_info_counter.set_start_time(datetime.datetime.now())

        for j in range(5):
            tc = HTTPTestCase("000" + str(i*100 + j), "{username:\"XXX\", userpassword:\"XXX\",}",
                              "jsonxpath:/userinfo/uid", "8008", "Verify user id is 8008")

            test_case_info_object.append_test_case(tc)

            _test_case_counter = TestCaseCounter()
            _test_case_counter.set_test_case(tc)
            _test_case_counter.set_start_time(datetime.datetime.now())
            time.sleep(1)
            _test_case_counter.set_end_time(datetime.datetime.now())
            if j % 2 == 0:
                _test_case_counter.set_result_object("pass", "test case pass!")
            else:
                _test_case_counter.set_result_object("fail", "test case fail!")

            _test_info_counter.set_end_time(datetime.datetime.now())
            _test_info_counter.set_api_http_url(test_case_info_object.get_api_http_url())
            _test_info_counter.set_api_desc(test_case_info_object.get_api_desc())
            _test_info_counter.set_api_http_method(test_case_info_object.get_api_http_method())
            _test_info_counter.append_test_case_counter(_test_case_counter)

        suite.append_test_case_info_counter(_test_info_counter)

    return suite


if __name__ == "__main__":
    _result_list = _mock_test_suite_counter_obj()
    _html_gen = HTMLReportGenerator(_result_list)
    print _html_gen.get_report()
