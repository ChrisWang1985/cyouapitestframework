# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
import traceback


class AssertException(Exception):
    def __init__(self, message):
        self._message = message

    def get_error_message(self):
        return self._message

    def get_trace(self):
        return traceback.format_exc()