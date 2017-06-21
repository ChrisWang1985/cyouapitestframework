# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""


class HTTPTestCaseInfo(object):
    def __init__(self, api_http_url, api_http_header, api_http_method, api_desc):
        self._api_http_url = api_http_url
        self._api_http_header = api_http_header
        self._api_http_method = api_http_method
        self._api_desc = api_desc
        self._api_test_case_list = []

    def append_test_case(self, http_test_case_obj):
        self._api_test_case_list.append(http_test_case_obj)

    def get_test_case_list(self):
        return self._api_test_case_list

    def get_api_http_url(self):
        return self._api_http_url

    def get_api_http_header(self):
        return self._api_http_header

    def get_api_http_method(self):
        return self._api_http_method

    def get_api_desc(self):
        return self._api_desc
