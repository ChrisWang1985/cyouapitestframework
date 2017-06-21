# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

from iparser import IParser
import xlrd
import re
from testbean.httptestbean.httptestcaseinfo import HTTPTestCaseInfo
from testbean.httptestbean.httptestcase import HTTPTestCase
from requestlib.httprequestlib import HTTPRequest
from verifylib.verifyhelper import HTTPVerifyHelper
import os
import sys
sys.path.append("Z:\\cyouapitestframework")


class ExcelParser(IParser):
    def __init__(self, path):
        self._file_path = path
        self._test_case_start_index = 5
        self._work_book = None
        self._test_case_info = None

    def _check_work_book_opened(self, work_book):
        if work_book is None:
            raise Exception("The work book is not opened!")

    def _open_work_book(self):
        return self.open_work_book_by_path(self._file_path)

    def open_work_book_by_path(self, path):
        try:
            _work_book = xlrd.open_workbook(path)
        except:
            raise Exception("Can not open work book! Pls check it at path: %s" % path)

        return _work_book

    def _open_sheet(self, work_book):
        return self.open_sheet_by_index(work_book, 0)

    def open_sheet_by_index(self, work_book, index):
        try:
            _sheet = work_book.sheet_by_index(index)
        except:
            raise Exception("Can not open sheet by index %d" % index)

        return _sheet

    def open_sheet_by_name(self, work_book, sheet_name):
        try:
            _sheet = work_book.sheet_by_name(sheet_name)
        except:
            raise Exception("Can not open sheet by name %s" % sheet_name)

        return _sheet

    def _find_column_index_from_header(self, header_row, col_name):
        _length = len(header_row)
        _index = -1

        for i in range(_length):
            _header_value = header_row[i]

            if _header_value.lower() == col_name.lower():
                _index = i

        return _index

    def _get_test_data_from_sheet(self, sheet, col_name, row_index):
        _rows_length = sheet.nrows

        if row_index > _rows_length:
            raise Exception("Can not find %dth rows from sheet %s" % (row_index, sheet.name))

        _header_row = sheet.row_values(0)
        _col_index = self._find_column_index_from_header(_header_row, col_name)

        #_sheet_result_value = sheet.row_values(row_index)[_col_index].replace("\n", "")

        # return _sheet_result_value.split()
        return sheet.row_values(row_index)[_col_index]

    def _get_extra_sheet_test_data(self, work_book, sheet_name, col_name):
        return self._get_extra_sheet_test_data_by_row_index(work_book, sheet_name, col_name, 0)

    def _get_extra_sheet_test_data_by_row_index(self, work_book, sheet_name, col_name, row_index):
        _sheet = self.open_sheet_by_name(work_book, sheet_name)

        return self._get_test_data_from_sheet(_sheet, col_name, row_index)

    def _get_extra_work_book_test_data(self, work_book_path, sheet_name, col_name, row_index):
        _extra_work_book = self.open_work_book_by_path(work_book_path)
        _extra_sheet = self.open_sheet_by_name(_extra_work_book, sheet_name)

        return self._get_test_data_from_sheet(_extra_sheet, col_name, row_index)

    def get_extra_file_content(self, file_path):
        _file = open(file_path, "r")
        _file_content = ""

        try:
            _file_lines = _file.readlines()
        except:
            raise Exception("Can not open file at path: %s" % file_path)
        finally:
            _file.close()

        for line in _file_lines:
            _file_content += line.strip("\n")

        return _file_content

    def _get_test_case_sheet(self):
        _work_book = self._open_work_book()
        _test_case_sheet = self._open_sheet(_work_book)

        return _test_case_sheet

    def _set_test_info(self):
        if 1 == 1:
            pass
        _test_case_sheet = self._get_test_case_sheet()
        _test_case_length = _test_case_sheet.nrows

        _api_http_url = _test_case_sheet.cell(0, 1).value
        _api_http_header = _test_case_sheet.cell(1, 1).value
        _api_http_method = _test_case_sheet.cell(2, 1).value
        _api_desc = _test_case_sheet.cell(3, 1).value

        _test_case_info_obj = HTTPTestCaseInfo(_api_http_url,
                                               _api_http_header,
                                               _api_http_method,
                                               _api_desc)

        #TODO: add test case to test info object
        for row_index in range(self._test_case_start_index, _test_case_length):
            _row_data = _test_case_sheet.row_values(row_index)
            _test_case_info_obj.append_test_case(self._set_test_case_details(_row_data))

        return _test_case_info_obj

    def _set_test_case_details(self, row_data):
        if row_data is not None:
            _test_case_id = row_data[0]
            _test_case_is_run = row_data[1]
            _test_case_http_body = self._parse_http_body_field(row_data[2])
            _test_case_assert_pattern = self._parse_assert_pattern_field(row_data[3])
            _test_case_assert_value = self._parse_assert_value_field(row_data[4])
            _test_case_desc = row_data[5]

            _http_test_case = HTTPTestCase(_test_case_id,
                                           _test_case_http_body,
                                           _test_case_assert_pattern,
                                           _test_case_assert_value,
                                           _test_case_desc,
                                           _test_case_is_run)

        return _http_test_case

    def _parse_http_body_field(self, http_body_content):
        return self._parse_test_content_from_field(http_body_content)

    def _parse_assert_pattern_field(self, assert_pattern):
        return self._parse_multiline_test_data(assert_pattern)

    def _parse_assert_value_field(self, assert_value):
        return self._parse_multiline_test_data(assert_value)

    def _parse_test_content_from_field(self, content):
        if content.startswith("$"):
            _col_name = re.findall(r"\.\w+", content)[0][1:]
            _sheet_name = re.findall(r"\$\w+\.", content)[0][1:-1]
            if content.find("[") > 0:
                _row_index = int(re.findall(r"\[(\d*)\]", content)[0])
            else:
                _row_index = 1

            _field_value = self._get_extra_sheet_test_data_by_row_index(self._work_book, _sheet_name, _col_name,
                                                                        _row_index)
        elif content.startswith(".load:"):
            if content.find("[") > 0:
                _row_index = int(re.findall(r"\[(\d*)\]", content)[0])
            else:
                _row_index = 1

            _work_book_path = os.path.abspath("..\\testcases\\") + re.findall(r":\D+\$", content)[0][1:-1]
            _sheet_name = str(re.findall(r"\$\w+\.", content)[0][1:-1])
            _col_name = re.findall(r"\.\w+\[", content)[0][1:-1]

            _field_value = self._get_extra_work_book_test_data(_work_book_path, _sheet_name, _col_name, _row_index)
        elif content.startswith(".file:"):
            _file_path = os.path.abspath("..\\testcases\\testfiles\\")
            _file_path += content[6:]

            _field_value = self.get_extra_file_content(_file_path)
        else:
            _field_value = content

        return _field_value

    def _parse_multiline_test_data(self, multiline_test_data):
        if multiline_test_data != "":
            _test_data_list = multiline_test_data.split()
            _test_data_list_length = len(_test_data_list)
            _result_list = []

            for i in range(_test_data_list_length):
                _result_list.append(self._parse_test_content_from_field(_test_data_list[i]))
        else:
            _result_list = [""]

        return _result_list

    def get_test_info(self):
        self._work_book = self._open_work_book()
        self._open_sheet(self._work_book)
        self._test_case_info = self._set_test_info()

        return self._test_case_info

if __name__ == "__main__":
    # _parse = ExcelParser("Z:\\cyouapitestframework\\testcases\\temptestcase.xls")
    # _test_case_info = _parse.get_test_info()
    # print _test_case_info.get_api_http_url()
    # print _test_case_info.get_api_http_header()
    # print _test_case_info.get_api_http_method()
    # print _test_case_info.get_api_desc()
    #
    # _test_case_list = _test_case_info.get_test_case_list()
    # _test_case_list_length = len(_test_case_list)
    #
    # for i in range(_test_case_list_length):
    #     print "==================================" + str(_test_case_list[i].get_case_id()) + "=================================="
    #     print _test_case_list[i].get_case_id()
    #     print _test_case_list[i].get_case_is_run()
    #     print _test_case_list[i].get_case_http_body()
    #     print _test_case_list[i].get_case_assert_pattern()
    #     print _test_case_list[i].get_case_assert_value()
    #     print _test_case_list[i].get_case_desc()

    _excel_parser = ExcelParser("Z:\\cyouapitestframework\\testcases\\temptestcase.xls")
    _test_case_info = _excel_parser.get_test_info()
    _request = HTTPRequest()
    _verify = HTTPVerifyHelper()

    _test_case_list = _test_case_info.get_test_case_list()
    _test_case_list_length = len(_test_case_list)

    _api_url = _test_case_info.get_api_http_url()
    _api_method = _test_case_info.get_api_http_method()
    _api_header = _test_case_info.get_api_http_header()
    _api_desc = _test_case_info.get_api_desc()

    print u"Test api HTTP url: %s" % _api_url
    print u"Test api HTTP method: %s" % _api_method
    print u"Test api HTTP header: %s" % _api_header
    print u"Test api desc: %s" % _api_desc

    for i in range(_test_case_list_length):
        try:
            print "=====================  start test case %d  =====================" % (i + 1)
            _http_test_case_obj = _test_case_list[i]

            print u"Test case id: %s" % _http_test_case_obj.get_case_id()
            print u"Test case http body: %s" % _http_test_case_obj.get_case_http_body()
            print u"Test case assert pattern: %s" % _http_test_case_obj.get_case_assert_pattern()
            print u"Test case assert value: %s" % _http_test_case_obj.get_case_assert_value()
            print u"Test case desc: %s" % _http_test_case_obj.get_case_desc()

            _response = _request.send_http_request(_api_url, _api_method,
                                                   request_body=_http_test_case_obj.get_case_http_body(),
                                                   header=_api_header)

            # print _response.text
            _result = _verify.verify(_response.text, _http_test_case_obj.get_case_assert_pattern(),
                                     _http_test_case_obj.get_case_assert_value())

            print u"Test result: %s" % str(_result)
            print "=====================  end test case %d  =====================" % (i + 1)
            print "   "
            print "   "
        except Exception, ex:
            pass