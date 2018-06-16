#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/14 17:44
@file: session_service.py
@desc: 会话服务层
"""
import datetime

import jwt
from flask import request, make_response, json

from com.lzy.project.admin.base.basic import BasicService
from com.lzy.project.admin.constant.constant import Constants
from com.lzy.project.admin.helper.db_helper import DbHelper
from com.lzy.project.admin.helper.sys_conf_helper import SysConfHelper
from com.lzy.project.admin.model.t_permissions_model import TPermissionsUser
from com.lzy.project.admin.response.response import ResponseCode, Code
from com.lzy.project.admin.service.permissions.permissions_resource_service import PermissionsResourceService
from com.lzy.project.admin.tools.date_utils import DateUtils
from com.lzy.project.admin.tools.log_util import debug


class SessionService(BasicService):
    single = None

    @classmethod
    def get_single(cls):
        """
        获取单实例
        :return:
        """
        if not cls.single:
            debug("sessionService", "实例化[sessionService]服务类")
            cls.single = SessionService()
        return cls.single

    @staticmethod
    def sessions():
        method = request.method.lower()
        return SessionService.get_single().callback("{0}_".format(method), "session")

    @staticmethod
    def put_session():
        """
        登录session
        :return:
        """
        params_data = request.get_json()['params']
        username = params_data['username']
        password = params_data['pass']

        row_user_info = DbHelper.get_db().session.query(TPermissionsUser).filter_by(
            login_name=username, valid_status=Constants.VALID_STATUS_Y).first()
        # 如果查不到
        if not row_user_info:
            # 返回用户不存在提示信息
            return make_response(
                json.dumps(ResponseCode.response(res_json=Code.ACCOUNT_NOT_EXISTS), ensure_ascii=False))
        # 如果存在，则检查密码
        user_model = TPermissionsUser()
        user_model.row_to_model(row_user_info)
        if not user_model.check_password(password):
            return make_response(
                json.dumps(ResponseCode.response(res_json=Code.LOGIN_PASS_ERROR), ensure_ascii=False))
        # 用户名密码正确，生成token
        salt = user_model.salt
        payload = {
            'user': {"username": user_model.login_name, "password": user_model.password},
            'aud': salt,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(SysConfHelper.get_item('jwt', 'exp')))
        }
        token = jwt.encode(payload, SysConfHelper.get_item('jwt', 'secret_key'), algorithm='HS256')
        user = user_model.to_json()
        # 权限资源
        nav_menus = PermissionsResourceService.resources_by_user(uid=user['id'], res_type=Constants.RES_TYPE_MENU)
        # f_uris = PermissionsResourceService.resources_by_user(uid=user['id'],
        #                                                    user_type=user_type, res_type=Constants.RES_TYPE_FURI)
        uris = PermissionsResourceService.resources_by_user(uid=user['id'], res_type=Constants.RES_TYPE_URI)

        data = dict()
        data['token'] = str(bytes(token), encoding='utf-8')
        data['user'] = json.dumps(user)
        data['salt'] = salt
        data['nav_menus'] = json.dumps(nav_menus)
        # data['f_uris'] = json.dumps(f_uris)
        data['uris'] = json.dumps(uris)
        data['upd_resource_time'] = DateUtils.get_current_time()
        return make_response(
            json.dumps(ResponseCode.response(data=data), ensure_ascii=False))

    def delete_session(self):
        pass
