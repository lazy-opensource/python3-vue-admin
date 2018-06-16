#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/5 16:47
@file: app_router.py
@desc: 
"""
import jwt
from flask import Blueprint, make_response, json, request

from com.lzy.project.admin.helper.db_helper import DbHelper
from com.lzy.project.admin.helper.sys_conf_helper import SysConfHelper
from com.lzy.project.admin.response.response import ResponseCode, Code
from com.lzy.project.admin.service.example_service import ExampleService
from com.lzy.project.admin.service.permissions.permissions_group_service import PermissionsGroupService
from com.lzy.project.admin.service.permissions.permissions_resource_service import PermissionsResourceService
from com.lzy.project.admin.service.permissions.permissions_role_service import PermissionsRoleService
from com.lzy.project.admin.service.permissions.permissions_user_service import PermissionsUserService
from com.lzy.project.admin.service.session_service import SessionService
from com.lzy.project.admin.tools.log_util import error

app_router = Blueprint('app_router', __name__)

white_list = [
    {"method": "PUT", "url": "/api/admin/sessions"}
]


def before():
    """
    验证token
    :return:
    """
    url = request.url_rule
    method = request.method
    if method == 'OPTIONS':
        return
    for i, white in enumerate(white_list):
        if white['method'] == str(method) and white['url'] == str(url):
            break
    else:
        token_str = request.headers.get('Py-Vue-Token')
        if not token_str:
            return make_response(json.dumps(ResponseCode.response(res_json=Code.NO_TOKEN)))
        token_json = json.loads(token_str)
        if not 'token' in token_json.keys():
            return make_response(json.dumps(ResponseCode.response(res_json=Code.NO_TOKEN)))
        token = bytes(token_json['token'], encoding='utf-8')
        salt = token_json['salt']
        try:
            user = jwt.decode(token, SysConfHelper.get_item('jwt', 'secret_key'), audience=salt,
                              algorithm='HS256')
            if not user:
                return make_response(json.dumps(ResponseCode.response(res_json=Code.SIGN_ERROR)))
        except jwt.InvalidAudienceError as ie:
            error('before', 'InvalidAudienceError:' + str(ie))
            return make_response(json.dumps(ResponseCode.response(res_json=Code.SALT_ERROR)))
        except jwt.ExpiredSignatureError as se:
            error('before', 'InvalidAudienceError:' + str(se))
            return make_response(json.dumps(ResponseCode.response(res_json=Code.EXP_TOKEN)))
        return


def after(response):
    """
    解决跨域
    :param response:
    :return:
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, POST, GET, DELETE, OPTIONS'
    response.headers[
        'Access-Control-Allow-Headers'] = 'Content-Type, Content-Length,' \
                                          ' Py-Vue-Token, Authorization, Accept, X-Requested-With'
    return response


@app_router.errorhandler(404)
def internal_404_error(error):
    return make_response(json.dumps(ResponseCode.response(404, "找不到资源")))


@app_router.errorhandler(400)
def internal_400_error(error):
    return make_response(json.dumps(ResponseCode.response(404, "请求参数解析错误")))


@app_router.errorhandler(500)
def internal_500_error(error):
    DbHelper.get_db().session.rollback()
    return make_response(json.dumps(ResponseCode.response(500, "服务器错误")))


app_router.before_request(before)
app_router.after_request(after)

app_router.add_url_rule(rule='/hello', view_func=ExampleService.hello, methods=['GET'])
app_router.add_url_rule(rule='/examples', view_func=ExampleService.examples, methods=['GET', 'PUT', 'POST', 'DELETE'])

# 系统权限模块 #####################################################
# 系统权限-用户
app_router.add_url_rule(rule='/permissions/users', view_func=PermissionsUserService.users,
                        methods=['GET', 'PUT', 'POST', 'DELETE'])
app_router.add_url_rule(rule='/permissions/user/check/uniq', view_func=PermissionsUserService.user_check_uniq,
                        methods=['GET'])
app_router.add_url_rule(rule='/permissions/user/groups', view_func=PermissionsUserService.user_groups,
                        methods=['GET', 'PUT', 'POST', 'DELETE'])
app_router.add_url_rule(rule='/permissions/user/roles', view_func=PermissionsUserService.user_roles,
                        methods=['GET', 'PUT', 'POST', 'DELETE'])
app_router.add_url_rule(rule='/permissions/user/roles/uid', view_func=PermissionsUserService.user_roles_uid,
                        methods=['GET'])

# 系统权限-角色
app_router.add_url_rule(rule='/permissions/roles', view_func=PermissionsRoleService.roles,
                        methods=['GET', 'PUT', 'POST', 'DELETE'])
app_router.add_url_rule(rule='/permissions/role/check/uniq',
                        view_func=PermissionsRoleService.role_check_uniq, methods=['GET'])
app_router.add_url_rule(rule='/permissions/role/groups', view_func=PermissionsRoleService.role_groups,
                        methods=['GET', 'PUT', 'POST', 'DELETE'])
app_router.add_url_rule(rule='/permissions/role/resources', view_func=PermissionsRoleService.role_resources,
                        methods=['GET', 'POST'])

# 系统权限-用户组
app_router.add_url_rule(rule='/permissions/groups', view_func=PermissionsGroupService.groups,
                        methods=['GET', 'PUT', 'POST', 'DELETE'])
app_router.add_url_rule(rule='/permissions/group/resources', view_func=PermissionsGroupService.group_resources,
                        methods=['GET', 'POST', 'DELETE'])
app_router.add_url_rule(rule='/permissions/group/resourcesbygid',
                        view_func=PermissionsGroupService.get_resources_by_groupid, methods=['GET', 'POST'])
app_router.add_url_rule(rule='/permissions/group/users', view_func=PermissionsGroupService.group_users,
                        methods=['GET'])
app_router.add_url_rule(rule='/permissions/group/roles', view_func=PermissionsGroupService.group_roles,
                        methods=['GET'])
app_router.add_url_rule(rule='/permissions/group/check/uniq', view_func=PermissionsGroupService.group_check_uniq,
                        methods=['GET'])

# 系统权限-资源
app_router.add_url_rule(rule='/permissions/resources', view_func=PermissionsResourceService.resources,
                        methods=['GET', 'PUT', 'POST', 'DELETE'])
app_router.add_url_rule(rule='/permissions/resources/id', view_func=PermissionsResourceService.resource_by_id,
                        methods=['GET'])
app_router.add_url_rule(rule='/permissions', view_func=PermissionsResourceService.get_permission, methods=['GET'])
app_router.add_url_rule(rule='/permissions/submenus', view_func=PermissionsResourceService.get_permission_submenus,
                        methods=['GET'])
app_router.add_url_rule(rule='/permissions/resource/check/uniq',
                        view_func=PermissionsResourceService.resource_check_uniq, methods=['GET'])

# 系统权限模块 #####################################################

# 登录模块 ##########################################################
app_router.add_url_rule(rule='/sessions', view_func=SessionService.sessions, methods=['GET', 'PUT', 'POST', 'DELETE'])
