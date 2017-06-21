# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""


class HTMLMarkupDictionary(object):
    HTML_TABLE_TEMPLATE = "<table id=\"%s\" class=\"%s\">%s</table>"
    HTML_TABLE_TR_TEMPLATE = "<tr class=\"%s\">%s</tr>"
    HTML_TABLE_TD_TEMPLATE = "<td class=\"%s\">%s</td>"
    HTML_TABLE_TD_COL_SPAN_TEMPLATE = "<td colspan=\"%s\" class=\"%s\">%s</td>"