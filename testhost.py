# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
import os
import argparse
from caseconfparser.caseconfparser import CaseConfParser
from runner.httpapitestrunner import HTTPAPITestRunner
from casereport.htmlreportgen import HTMLReportGenerator
from mailsender.mailsender import MailSender
from testbean.configbean.globalconfbean import GlobalConfBean


parser = argparse.ArgumentParser()
parser.add_argument("--confpath", help=u"配置文件路径")
_conf_path = parser.parse_args().confpath

if __name__ == "__main__":
    try:
        _conf_path = "E:\\project\\python\\cyouapitestframework\\config\\conf.ini"
        if os.path.exists(_conf_path):
            _case_conf_parser = CaseConfParser(_conf_path)
        else:
            raise IOError("Can not found file from path:%s" % _conf_path)

        _runner = HTTPAPITestRunner()
        _result_list_object = _runner.run_test_cases(_case_conf_parser.get_project_work_dir())

        if len(_result_list_object.get_test_case_info_counter()) > 0:
            _html_report = HTMLReportGenerator(_result_list_object)
            _report_content = _html_report.get_report()
        # print _report_content

            # _mail_sender = MailSender()
            # _mail_sender.send_mail(GlobalConfBean.mail_subject, GlobalConfBean.mail_to_list, _report_content)
            _report_file = open(GlobalConfBean.report_path, 'w')
            _report_file.write(_report_content.encode('utf-8'))
            _report_file.close()
        else:
            print 'It seems obtain 0 test case from test case files!'
    except Exception, ex:
        print ex
