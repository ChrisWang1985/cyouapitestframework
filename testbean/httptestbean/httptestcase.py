# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

from common.keydictionary import KeyDictionary


class HTTPTestCase(object):
    def __init__(self, case_id, http_body, assert_pattern, assert_value, case_desc, is_run=True):
        self.test_case_dict = {
            KeyDictionary.CASE_ID: case_id,
            KeyDictionary.IS_RUN: is_run,
            KeyDictionary.HTTP_BODY: http_body,
            KeyDictionary.ASSERT_PATTERN: assert_pattern,
            KeyDictionary.ASSERT_VALUE: assert_value,
            KeyDictionary.CASE_DESC: case_desc
        }

    def get_case_id(self):
        return int(self.test_case_dict[KeyDictionary.CASE_ID])

    def get_case_is_run(self):
        return self.test_case_dict[KeyDictionary.IS_RUN]

    def get_case_http_body(self):
        return self.test_case_dict[KeyDictionary.HTTP_BODY]

    def get_case_assert_pattern(self):
        return self.test_case_dict[KeyDictionary.ASSERT_PATTERN]

    def get_case_assert_value(self):
        return self.test_case_dict[KeyDictionary.ASSERT_VALUE]

    def get_case_desc(self):
        return self.test_case_dict[KeyDictionary.CASE_DESC]


if __name__ == "__main__":
    httpTC = HTTPTestCase("0001", "{username:\"XXX\", userpassword:\"XXX\",}",
                          "jsonxpath:/userinfo/uid", \
                          "8008", "Verify user id is 8008")
    print "CaseID: " + httpTC.get_case_id()
    print "HTTPBody: " + httpTC.get_case_http_body()
    print "AssertPattern: " + httpTC.get_case_assert_pattern()
    print "AssertValue: " + httpTC.get_case_assert_value()
    print "CaseDesc: " + httpTC.get_case_desc()
    print "IsRun: " + str(httpTC.get_case_is_run())

