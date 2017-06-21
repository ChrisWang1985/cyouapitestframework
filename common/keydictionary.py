# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""


class KeyDictionary(object):
    CASE_ID = "case_id"
    IS_RUN = "is_run"
    HTTP_BODY = "http_body"
    ASSERT_PATTERN = "assert_pattern"
    ASSERT_VALUE = "assert_value"
    CASE_DESC = "case_desc"


if __name__ == "__main__":
    print KeyDictionary.CASE_ID
    print KeyDictionary.IS_RUN
    print KeyDictionary.HTTP_BODY
    print KeyDictionary.ASSERT_VALUE
    print KeyDictionary.CASE_DESC
    print KeyDictionary.ASSERT_PATTERN