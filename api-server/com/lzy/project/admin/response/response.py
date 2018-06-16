#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/5 16:47
@file: response.py
@desc: 解决跨域问题
"""
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response


class AppResponse(Response):
    def __init__(self, response=None, **kwargs):
        kwargs['headers'] = ''
        headers = kwargs.get('headers')
        # 跨域控制
        origin = ('Access-Control-Allow-Origin', '*')
        methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
        if headers:
            headers.add(*origin)
            headers.add(*methods)
        else:
            headers = Headers([origin, methods])
        kwargs['headers'] = headers
        return super().__init__(response, **kwargs)


class ResponseCode:

    @staticmethod
    def response(code=200, msg='请求处理成功', data=None, res_json=None):
        if res_json:
            return res_json
        else:
            return dict(code=code, msg=msg, data=data)


class Code:
    ACCOUNT_NOT_EXISTS = {"code": 1000, "msg": "用户不存在", "data": None}
    LOGIN_PASS_ERROR = {"code": 1001, "msg": "登录密码错误", "data": None}
    SIGN_ERROR = {"code": 1002, "msg": "token错误", "data": None}
    SALT_ERROR = {"code": 1003, "msg": "加密盐错误", "data": None}
    NO_TOKEN = {"code": 1004, "msg": "不合法客户端", "data": None}
    EXP_TOKEN = {"code": 1005, "msg": "token已过期", "data": None}


if __name__ == "__main__":
    print(ResponseCode.response(200, "请求处理成功", "data"))
