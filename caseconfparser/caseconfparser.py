# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
from ConfigParser import ConfigParser
from datetime import date
from testbean.configbean.globalconfbean import GlobalConfBean


class CaseConfParser(object):
    def __init__(self, path):
        self._conf_path = path
        self._conf_parser = ConfigParser()
        self._conf_parser.read(path)
        self.init_global_conf_bean()

    def _get_field_from_section(self, section, field):
        try:
            _result_value = self._conf_parser.get(section, field)
        except Exception:
            _result_value = ""

        return _result_value

    def get_project_name(self):
        return self._get_field_from_section("project", "name")

    def get_project_url(self):
        return self._get_field_from_section("project", "url")

    def get_project_work_dir(self):
        return self._get_field_from_section("project", "workdir")

    def get_project_header(self):
        return self._get_field_from_section("project", "header")

    def get_project_login_url(self):
        return self._get_field_from_section("project", "loginurl")

    def get_project_user_name(self):
        return self._get_field_from_section("project", "username")

    def get_project_password(self):
        return self._get_field_from_section("project", "password")

    def get_mail_subject(self):
        return self._get_field_from_section("mail", "subject") + " " + str(date.today())

    def get_mail_to_list(self):
        return self._get_field_from_section("mail", "to")

    def get_mail_cc_list(self):
        return self._get_field_from_section("mail", "cc")

    def get_report_path(self):
        return self._get_field_from_section("mail", "reportpath")

    def init_global_conf_bean(self):
        GlobalConfBean.project_name = self.get_project_name()
        GlobalConfBean.work_dir = self.get_project_work_dir()
        GlobalConfBean.url = self.get_project_url()
        GlobalConfBean.header = self.get_project_header()
        GlobalConfBean.login_url = self.get_project_login_url()
        GlobalConfBean.user_name = self.get_project_user_name()
        GlobalConfBean.password = self.get_project_password()
        GlobalConfBean.mail_subject = self.get_mail_subject()
        GlobalConfBean.mail_to_list = self.get_mail_to_list()
        GlobalConfBean.report_path = self.get_report_path()
