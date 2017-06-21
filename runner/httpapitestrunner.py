# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
# import sys
# sys.path.append("Z:\\cyouapitestframework")
import os
import datetime
from caseparser.excelCaseParser import ExcelCaseParser
from requestlib.httprequestlib import HTTPRequest
from verifylib.verifyhelper import HTTPVerifyHelper
from testbean.httptestbean.testcaseinfocounter import TestCaseInfoCounter
from testbean.httptestbean.testcasecounter import TestCaseCounter
from testbean.httptestbean.testsuitcounter import TestSuiteCounter
from caseexceptions.httprequestexception import HTTPRequestException
from caseexceptions.assertfailException import AssertFailException
from caseexceptions.assertexception import AssertException
from casereport.htmlreportgen import HTMLReportGenerator
from testbean.configbean.globalconfbean import GlobalConfBean


class HTTPAPITestRunner:
    def __init__(self):
        self._excel_test_file_list = []

    def _get_all_files_from_path(self, path):
        for root, dirs, files in os.walk(path):
            print "root %d" % len(root)
            print "dirs %d" % len(dirs)
            print "files %d" % len(files)
            for name in files:
                if name[-4:] == ".xls":
                    self._excel_test_file_list.append(root + "\\" + name)

    def run_test_cases(self, path):
        _suite_result_list = TestSuiteCounter()
        self._get_all_files_from_path(path)

        for file_path in self._excel_test_file_list:
            try:
                _excel_parser = ExcelCaseParser(file_path)
                _test_case_info = _excel_parser.get_test_info()
                _request = HTTPRequest()
                _verify = HTTPVerifyHelper()

                _test_case_list = _test_case_info.get_test_case_list()
                _test_case_list_length = len(_test_case_list)

                _api_url = GlobalConfBean.url + _test_case_info.get_api_http_url()
                _api_method = _test_case_info.get_api_http_method()
                _api_header = _test_case_info.get_api_http_header()

                if _api_header == "":
                    _api_header = GlobalConfBean.header

                _api_desc = _test_case_info.get_api_desc()

                _test_info_counter = TestCaseInfoCounter()
                _test_info_counter.set_api_http_url(_test_case_info.get_api_http_url())
                _test_info_counter.set_api_http_method(_api_method)
                _test_info_counter.set_api_desc(_api_desc)
                _test_info_counter.set_start_time(datetime.datetime.now())

                for i in range(_test_case_list_length):
                    _http_test_case_obj = _test_case_list[i]

                    _test_case_counter = TestCaseCounter()
                    _test_case_counter.set_test_case(_http_test_case_obj)
                    _test_case_counter.set_start_time(datetime.datetime.now())

                    try:
                        if GlobalConfBean.user_name != "" and GlobalConfBean.password != "":
                            _response = _request.send_http_request_with_auth(GlobalConfBean.login_url,
                                                                             GlobalConfBean.user_name,
                                                                             GlobalConfBean.password,
                                                                             _api_url,
                                                                             _api_method,
                                                                             request_body=
                                                                             _http_test_case_obj.get_case_http_body(),
                                                                             header=_api_header)
                        else:
                            _response = _request.send_http_request(_api_url, _api_method,
                                                                   request_body=_http_test_case_obj.get_case_http_body(),
                                                                   header=_api_header)

                        # if i == 1:
                        #     _http_test_case_obj.test_case_dict["assert_pattern"] = "abc"

                        _result = _verify.verify(_response.text, _http_test_case_obj.get_case_assert_pattern(),
                                                 _http_test_case_obj.get_case_assert_value())

                        _test_case_counter.set_result_object(_result, "Test case pass!")

                        # _test_info_counter.append_test_case_counter(_test_case_counter)
                    except AssertFailException, fail_exception:
                        _test_case_counter.set_result_object("fail", fail_exception.get_error_message())
                    except HTTPRequestException, http_exception:
                        _test_case_counter.set_result_object("error", http_exception.message + "<br>" +
                                                             http_exception.get_trace())
                    except AssertException, assert_exception:
                        _test_case_counter.set_result_object("error", assert_exception.message + "<br>" +
                                                             assert_exception.get_trace())
                    except Exception, ex:
                        _test_case_counter.set_result_object("error", ex.message)
                    finally:
                        _test_case_counter.set_end_time(datetime.datetime.now())
                        _test_info_counter.append_test_case_counter(_test_case_counter)

                _test_info_counter.set_end_time(datetime.datetime.now())
                _suite_result_list.append_test_case_info_counter(_test_info_counter)
            except Exception, ex:
                print "It seems can not load test case from test case files? Please check it."
                print ex.message
                continue

        return _suite_result_list

if __name__ == "__main__":
    _case_index = 1
    _runner = HTTPAPITestRunner()
    _result_list_object = _runner.run_test_cases("E:\\project\\python\\cyouapitestframework\\testcases")

    for _result_obj in _result_list_object.get_test_case_info_counter():
        print "================%dth API test result================" % _case_index
        print "API Http url is: %s" % _result_obj.get_api_http_url()
        print "API Http method is: %s" % _result_obj.get_api_http_method()
        print "API description is: %s" % _result_obj.get_api_desc()
        print "API result is: %s" % _result_obj.get_result_object()["result"]
        print "API pass rate is: %s" % _result_obj.get_result_object()["msg"]
        print "API test start time: %s" % _result_obj.get_start_time()
        print "API test end time: %s" % _result_obj.get_end_time()
        print "API test duration time: %s" % _result_obj.get_duration_time()

        _test_case_list_obj = _result_obj.get_test_case_counter_list()

        for _index in range(len(_test_case_list_obj)):
            _test_case_obj = _test_case_list_obj[_index]
            print "        =================Case %s================" % _test_case_obj.get_test_case().get_case_id()
            print "        test case start time: %s" % _test_case_obj.get_start_time()
            print "        test case end time: %s" % _test_case_obj.get_end_time()
            print "        test case duration time: %s" % _test_case_obj.get_duration_time()
            print "        test case result: %s" % _test_case_obj.get_result_object_with_key("result")
            print "        test case message: %s" % _test_case_obj.get_result_object_with_key("msg")
            print "        test case desc: %s" % _test_case_obj.get_test_case().get_case_desc()
            print "        =================Case End================"

        print "================%dth API test End================" % _case_index
        _case_index += 1

    _html_report = HTMLReportGenerator(_result_list_object)
    print _html_report.get_report()