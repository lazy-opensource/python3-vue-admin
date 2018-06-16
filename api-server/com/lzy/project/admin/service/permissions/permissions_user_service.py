#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/13 10:28
@file: permissions_user_service.py
@desc: 系统权限用户信息服务层
"""
import uuid

from flask import request, json, make_response
from werkzeug.security import generate_password_hash

from com.lzy.project.admin.base.basic import BasicService
from com.lzy.project.admin.constant.constant import Constants
from com.lzy.project.admin.helper.crud_helper import CRUDHelper
from com.lzy.project.admin.helper.db_helper import DbHelper
from com.lzy.project.admin.helper.sql_helper import SqlHelper
from com.lzy.project.admin.model.t_permissions_model import TPermissionsUser, TPermissionsUserGroupRel, \
    TPermissionsUserRoleRel, TPermissionsRoleGroupRel, TPermissionsRole
from com.lzy.project.admin.response.response import ResponseCode
from com.lzy.project.admin.service.permissions.permissions_rel_service import PermissionsRelService
from com.lzy.project.admin.tools.date_utils import DateUtils
from com.lzy.project.admin.tools.log_util import debug
from com.lzy.project.admin.tools.uuid_utils import uuidUtils


class PermissionsUserService(BasicService):
    single = None

    @classmethod
    def get_single(cls):
        """
        获取单实例
        :return:
        """
        if not cls.single:
            debug("permissionsUserService", "实例化[permissionsUserService]服务类")
            cls.single = PermissionsUserService()
        return cls.single

    @staticmethod
    def users():
        """
        CRUD t_permissions_user表核心路由
        :return: json格式数据
        """
        method = request.method.lower()
        return PermissionsUserService.get_single().callback("{0}_".format(method), "user")

    @staticmethod
    def user_groups():
        """
        CRUD 用户关联的用户组数据
        :return: json格式数据
        """
        method = request.method.lower()
        return PermissionsUserService.get_single().callback("{0}_".format(method), "user_group")

    @staticmethod
    def user_check_uniq():
        """
        检查唯一性约束
        :return: 结果对象
        """
        params = request.values.get('params')
        conditions = json.loads(params)
        model = TPermissionsUser()
        rows = CRUDHelper.execute_select(model=model, conditions=conditions)
        return make_response(json.dumps(ResponseCode.response(data=rows), ensure_ascii=False))

    @staticmethod
    def get_user():
        """
        获取用户列表
        :return:
        """
        params = request.values.get('params')
        conditions = json.loads(params)
        model = TPermissionsUser()
        rows = CRUDHelper.execute_select(model, conditions)
        total = CRUDHelper.execute_select_count(model, conditions)
        DbHelper.get_db().session.close()
        data = {"total": total, "rows": rows}
        return make_response(json.dumps(ResponseCode.response(data=data), ensure_ascii=False))

    @staticmethod
    def put_user():
        """
        新增用户
        :return:
        """
        params_data = request.get_json()['params']
        user = TPermissionsUser()
        user.set_attr_by_dist(params_data)
        user.password = generate_password_hash(user.password)
        user.create_time = DateUtils.get_current_time()
        user.last_update_time = user.create_time
        user.salt = uuidUtils.gen_uuid()
        DbHelper.get_db().session.add(user)
        DbHelper.get_db().session.commit()
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def post_user():
        """
        修改用户
        :return:
        """
        params_data = request.get_json()['params']
        params_data['last_update_time'] = DateUtils.get_current_time()
        DbHelper.get_db().session.query(TPermissionsUser).filter_by(id=params_data['id']).update(params_data)
        DbHelper.get_db().session.commit()
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def delete_user():
        """
        删除用户
        :return:
        """
        params_data = json.loads(request.args.get('ids'))
        if not params_data or len(params_data) < 1:
            raise Exception("参数 ids is blank")
        # 删除用户和用户组的关联关系
        PermissionsRelService.del_in_uids(TPermissionsUserGroupRel(), params_data)
        # 删除用户和角色的关联关系
        PermissionsRelService.del_in_uids(TPermissionsUserRoleRel(), params_data)
        CRUDHelper.execute_delete_by_field_in(TPermissionsUser(), params_data, 'id')
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def get_user_group():
        """
        获取用户关联的用户组数据
        :return:
        """
        params = request.values.get('params')
        params_data = json.loads(params)
        group_ids = PermissionsRelService.ids_by_userid(TPermissionsUserGroupRel(), params_data['user_id'], 'gid')
        return make_response(json.dumps(ResponseCode.response(data=group_ids), ensure_ascii=False))

    @staticmethod
    def post_user_group():
        """
        更新用户和用户组的关联关系
        :return:
        """
        params_data = request.get_json()['params']
        user_id = params_data['user_id']
        group_ids = params_data['group_ids']
        if not user_id or len(user_id) < 1:
            raise Exception("参数 user_id is blank")

        # 删除用户和角色的关联关系
        PermissionsRelService.del_in_uids(TPermissionsUserRoleRel(), [user_id])
        # 清空老的用户和用户组之间的关联关系
        PermissionsRelService.del_in_uids(TPermissionsUserGroupRel(), [user_id])
        # 重新关联
        if group_ids and len(group_ids) > 0:
            for group_id in group_ids:
                DbHelper.get_db().session.add(TPermissionsUserGroupRel(
                    uid=user_id, gid=group_id, create_time=DateUtils.get_current_time(),
                    last_update_time=DateUtils.get_current_time()))
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def user_roles_uid():
        """
        获取用户的关联角色ids
        :return:
        """
        params = request.values.get("user_id")
        if not params or len(params) < 1:
            return make_response(json.dumps(ResponseCode.response(data=[]), ensure_ascii=False))
        role_ids = PermissionsRelService.ids_by_userid(TPermissionsUserRoleRel(), uid=params, select_column_name='rid')
        return make_response(json.dumps(ResponseCode.response(data=role_ids), ensure_ascii=False))

    @staticmethod
    def user_roles():
        """
        CRUD 用户关联的角色数据
        :return: json格式数据
        """
        method = request.method.lower()
        return PermissionsUserService.get_single().callback("{0}_".format(method), "user_role")
    
    @staticmethod
    def get_user_role():
        """
        获取当前用户可以关联的角色
        :return: 
        """
        params = request.values.get("params")
        params_data = json.loads(params)
        user_id = params_data['user_id']
        conditions = params_data['condition']

        data = {"total": 0, "rows": []}
        # 根据用户id获取所在的用户组
        group_ids = PermissionsRelService.ids_by_userid(TPermissionsUserGroupRel(), user_id, 'gid')
        if not group_ids or len(group_ids) < 1:
            return make_response(json.dumps(ResponseCode.response(data=data), ensure_ascii=False))
        # 根据用户组获取角色id
        role_ids = PermissionsRelService.ids_in_groupids(TPermissionsRoleGroupRel(), group_ids, "rid")
        if not role_ids or len(role_ids) < 1:
            return make_response(json.dumps(ResponseCode.response(data=data), ensure_ascii=False))
        # 条件查找
        conditions['id'] = role_ids
        conditions['rule']['id'] = Constants.QUERY_CONDITION_RULE_IN
        model = TPermissionsRole()
        rows = CRUDHelper.execute_select(model, conditions)
        total = CRUDHelper.execute_select_count(model, conditions)
        data['rows'] = rows
        data['total'] = total
        return make_response(json.dumps(ResponseCode.response(data=data), ensure_ascii=False))

    @staticmethod
    def post_user_role():
        """
        关联角色
        :return:
        """
        params_data = request.get_json()['params']
        user_id = params_data['user_id']
        role_ids = params_data['role_ids']

        if not user_id or len(user_id) < 1:
            raise Exception("参数 user_id is blank")

        # 删除旧的用户和角色的关联关系
        PermissionsRelService.del_in_uids(TPermissionsUserRoleRel(), [user_id])
        # 重新关联用户和角色
        if role_ids and len(role_ids) > 0:
            for role_id in role_ids:
                DbHelper.get_db().session.add(TPermissionsUserRoleRel(
                    uid=user_id, rid=role_id, create_time=DateUtils.get_current_time(),
                    last_update_time=DateUtils.get_current_time()))
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))
