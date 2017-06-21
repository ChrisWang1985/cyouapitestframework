# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2014 by Administrator.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
import requests
from requests.auth import HTTPBasicAuth
from caseexceptions.httprequestexception import HTTPRequestException


class HTTPRequest:
    def __init__(self):
        pass

    def get_login_cookie(self, url, user_name, pass_word):
        _response = requests.get(url, auth=HTTPBasicAuth(user_name, pass_word))
        _cookie_obj = _response.cookies

        return _cookie_obj

    def send_http_request_with_auth(self, login_url, user_name, pass_word, logic_url, method, request_body="",
                                    header=""):
        _cookie_obj = self.get_login_cookie(login_url, user_name, pass_word)

        return self.send_http_request(logic_url, method, request_body=request_body, header=header, cookie=_cookie_obj)

    def send_http_request(self, url, method, request_body="", header="", cookie=None):
        try:
            if method.lower() == "get":
                if header is not "":
                    _response = requests.get(url, data=request_body, headers=eval(header), cookies=cookie)

                    return _response
                else:
                    _response = requests.get(url, data=request_body, cookies=cookie)

                    return _response
            elif method.lower() == "post":
                if header is not "":
                    _response = requests.post(url, data=request_body, headers=eval(header), cookies=cookie)

                    return _response
                else:
                    _response = requests.post(url, data=request_body, cookies=cookie)

                    return _response
            elif method.lower() == "put":
                if header is not "":
                    _response = requests.put(url, headers=eval(header), data=request_body, cookies=cookie)

                    return _response
                else:
                    _response = requests.put(url, data=request_body, cookies=cookie)

                    return _response
            elif method.lower() == "delete":
                if header is not "":
                    _response = requests.delete(url, headers=eval(header), data=request_body, cookies=cookie)

                    return _response
                else:
                    _response = requests.delete(url, data=request_body, cookies=cookie)

                    return _response
            elif method.lower() == "head":
                if header is not "":
                    _response = requests.head(url, headers=eval(header), data=request_body, cookies=cookie)

                    return _response
                else:
                    _response = requests.head(url, data=request_body, cookies=cookie)

                    return _response
            elif method.lower() == "options":
                if header is not "":
                    _response = requests.options(url, headers=eval(header), data=request_body, cookies=cookie)

                    return _response
                else:
                    _response = requests.options(url, data=request_body, cookies=cookie)

                    return _response
            else:
                raise Exception("Not supported method: %s" % method)
        except Exception, ex:
            raise HTTPRequestException(ex.message)

    def send_http_request_used_exec(self, url, method, request_body="", header="", cookie=None):
        if method not in ["get", "post", "put", "delete", "head", "options"]:
            raise Exception("Not supported method: %s" % method)

        _cookie_obj = cookie
        _response = None

        if header is not "":
            _request_api_string = "_response = requests.%s(%s, data=%s, header=%s, _cookie_obj)" % (method, url,
                                                                                                    request_body,
                                                                                                    header)
        else:
            _request_api_string = "_response = requests.%s(%s, data=%s, _cookie_obj)" % (method, url, request_body)

        exec _request_api_string

        return _response