# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
import smtplib
from email.mime.text import MIMEText


class MailSender(object):
    def __init__(self):
        self._smtp_server_address = "10.59.95.5"
        self._port = "25"
        self._from_mail_address = "wangjiaming@cyou-inc.com"

    def send_mail(self, subject, to_list, msg):
        sender = self._from_mail_address
        receiver = to_list.split(",")
        subject = subject

        # _msg_Root = MIMEMultipart('related')
        # _msg_Root['Subject'] = subject

        _msg_Text = MIMEText(msg, 'html', 'utf-8')
        _msg_Text["Subject"]=subject
        _msg_Text["From"] = sender
        _msg_Text["To"] = to_list

        # _msg_Root.attach(_msg_Text)

        _smtp = smtplib.SMTP()
        _smtp.connect('10.59.95.5:25')
        _smtp.sendmail(sender, receiver, _msg_Text.as_string())
        _smtp.quit()
        print "send mail ok!"


if __name__ == '__main__':
    mail_sender = MailSender()
    mail_sender.send_mail("test", "wjm19851120@163.com", 'Test')