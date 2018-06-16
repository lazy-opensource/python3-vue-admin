#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/13 18:07
@file: permissions_group_service.py
@desc: 系统权限用户组服务层
"""
from flask import request, json, make_response

from com.lzy.project.admin.base.basic import BasicService
from com.lzy.project.admin.constant.constant import Constants
from com.lzy.project.admin.helper.crud_helper import CRUDHelper
from com.lzy.project.admin.helper.db_helper import DbHelper
from com.lzy.project.admin.helper.sql_helper import SqlHelper
from com.lzy.project.admin.model.t_permissions_model import TPermissionsGroup, TPermissionsUserGroupRel, \
    TPermissionsRoleGroupRel, \
    TPermissionsResGroupRel, TPermissionsResource, TPermissionsUser, TPermissionsRole
from com.lzy.project.admin.response.response import ResponseCode
from com.lzy.project.admin.service.permissions.permissions_rel_service import PermissionsRelService
from com.lzy.project.admin.tools.date_utils import DateUtils
from com.lzy.project.admin.tools.log_util import debug


class PermissionsGroupService(BasicService):
    single = None

    @classmethod
    def get_single(cls):
        """
        获取单实例
        :return:
        """
        if not cls.single:
            debug("permissionsGroupService", "实例化[permissionsGroupService]服务类")
            cls.single = PermissionsGroupService()
        return cls.single

    @staticmethod
    def groups():
        """
        CRUD t_permissions__group表核心路由
        :return: json格式数据
        """
        method = request.method.lower()
        return PermissionsGroupService.get_single().callback("{0}_".format(method), "group")

    @staticmethod
    def group_check_uniq():
        """
        检查唯一性约束
        :return: 结果对象
        """
        params = request.values.get('params')
        conditions = json.loads(params)
        model = TPermissionsGroup()
        rows = CRUDHelper.execute_select(model=model, conditions=conditions)
        return make_response(json.dumps(ResponseCode.response(data=rows), ensure_ascii=False))

    @staticmethod
    def get_group():
        """
        获取用户组列表
        :return:
        """
        model = TPermissionsGroup()
        rows = CRUDHelper.execute_select(model, {})
        DbHelper.get_db().session.close()
        data = {"rows": PermissionsGroupService.gen_group_tree(rows)}
        return make_response(json.dumps(ResponseCode.response(data=data), ensure_ascii=False))

    @staticmethod
    def gen_group_tree(groups):
        groups_tree = []
        root_pid = str(Constants.ROOT_PID)
        for i, item in enumerate(groups):
            if item['pid'] == root_pid:
                obj = dict()
                obj['id'] = item['id']
                obj['label'] = item['group_name']
                obj['desc'] = item['group_desc']
                obj['code'] = item['group_code']
                obj['can_edit'] = item['can_edit']
                obj['disabled'] = False
                if item['can_edit'] == 'N':
                    obj['disabled'] = True
                groups_tree.append(obj)
        for i, item, in enumerate(groups_tree):
            PermissionsGroupService.recursion_group_tree(item, groups)
        return groups_tree

    @staticmethod
    def recursion_group_tree(current_group, groups):
        """
        生成用户组树
        :param current_group:
        :param groups:
        :return:
        """
        current_group['children'] = []
        for i, item in enumerate(groups):
            if item['pid'] != current_group['id']:
                continue
            else:
                obj = dict()
                obj['id'] = item['id']
                obj['label'] = item['group_name']
                obj['desc'] = item['group_desc']
                obj['code'] = item['group_code']
                obj['can_edit'] = item['can_edit']
                obj['disabled'] = False
                if item['can_edit'] == 'N':
                    obj['disabled'] = True
                current_group['children'].append(obj)
                # 递归
                PermissionsGroupService.recursion_group_tree(obj, groups)

    @staticmethod
    def put_group():
        """
        新增用户组
        :return:
        """
        params_data = request.get_json()['params']
        params_data['pid'] = params_data['pid'] if params_data['pid'] else Constants.ROOT_PID

        group = TPermissionsGroup()
        group.set_attr_by_dist(params_data)
        group.create_time = DateUtils.get_current_time()
        group.last_update_time = group.create_time
        DbHelper.get_db().session.add(group)
        DbHelper.get_db().session.commit()
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def post_group():
        """
        修改用户组
        :return:
        """
        params_data = request.get_json()['params']
        params_data['last_update_time'] = DateUtils.get_current_time()
        DbHelper.get_db().session.query(TPermissionsGroup).filter_by(id=params_data['id']).update(params_data)
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def delete_group():
        """
        删除用户组
        :return:
        """
        params_data = json.loads(request.args.get('ids'))
        if len(params_data) > 0:
            # 删除用户和用户组的关联关系
            PermissionsRelService.del_in_groupids(TPermissionsUserGroupRel(), params_data)
            # 删除角色和用户组的关联关系
            PermissionsRelService.del_in_groupids(TPermissionsRoleGroupRel(), params_data)
            # 删除资源和用户组的关联关系
            PermissionsRelService.del_in_groupids(TPermissionsResGroupRel(), params_data)
            CRUDHelper.execute_upd(TPermissionsGroup(), {'valid_status': Constants.VALID_STATUS_N}, params_data)
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def group_users():
        """
        用户组拥有用户列表
        :return:
        """
        params = request.values.get('params')
        conditions = json.loads(params)
        group_id = conditions['group_id']
        user_ids = PermissionsRelService.ids_in_groupids(
            model=TPermissionsUserGroupRel(), gids=[group_id], select_column_name='uid')
        if not user_ids:
            data = {"rows": [], "total": 0}
            return make_response(json.dumps(ResponseCode.response(data=data), ensure_ascii=False))

        conditions['group_id'] = None
        conditions['id'] = user_ids
        conditions['rule']['id'] = Constants.QUERY_CONDITION_RULE_IN
        model = TPermissionsUser()
        rows = CRUDHelper.execute_select(model, conditions)
        total = CRUDHelper.execute_select_count(model, conditions)

        data = {"rows": rows, "total": total}
        return make_response(json.dumps(ResponseCode.response(data=data), ensure_ascii=False))

    @staticmethod
    def group_roles():
        """
        用户组拥有角色列表
        :return:
        """
        params = request.values.get('params')
        conditions = json.loads(params)
        group_id = conditions['group_id']
        role_ids = PermissionsRelService.ids_in_groupids(
            model=TPermissionsRoleGroupRel(), gids=[group_id], select_column_name='rid')
        if not role_ids:
            data = {"rows": [], "total": 0}
            return make_response(json.dumps(ResponseCode.response(data=data), ensure_ascii=False))
        conditions['group_id'] = None
        conditions['id'] = role_ids
        conditions['rule']['id'] = Constants.QUERY_CONDITION_RULE_IN
        model = TPermissionsRole()
        rows = CRUDHelper.execute_select(model, conditions)
        total = CRUDHelper.execute_select_count(model, conditions)

        data = {"rows": rows, "total": total}
        return make_response(json.dumps(ResponseCode.response(data=data), ensure_ascii=False))

    @staticmethod
    def group_resources():
        """
        用户组关联资源总路由
        :return:
        """
        method = request.method.lower()
        return PermissionsGroupService.get_single().callback("{0}_".format(method), "group_resources")

    @staticmethod
    def post_group_resources():
        params_data = request.get_json()['params']
        params_data = params_data['params']
        group_id = params_data['group_id']
        res_ids = params_data['res_ids']
        if not group_id:
            raise Exception('param group_id is none')
        PermissionsRelService.del_in_groupids(model=TPermissionsResGroupRel(), groupids=[group_id])
        for i, rid in enumerate(res_ids):
            DbHelper.get_db().session.add(TPermissionsResGroupRel(
                rid=rid, gid=group_id,
                valid_status=Constants.VALID_STATUS_Y,
                create_time=DateUtils.get_current_time(),
                last_update_time=DateUtils.get_current_time()))
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def get_group_resources():
        """
        用户组关联资源前获取资源列表
        :return:
        """
        model = TPermissionsResource()
        rows = CRUDHelper.execute_select(model, {})
        data = {"rows": PermissionsGroupService.gen_resource_tree(rows)}
        return make_response(json.dumps(ResponseCode.response(data=data), ensure_ascii=False))

    @staticmethod
    def delete_group_resources():
        """
        删除用户组和资源的关联关系
        :return:
        """
        params_data = json.loads(request.args.get('params'))
        if params_data['gid'] == Constants.ADMIN_ID:
            """
            过滤系统菜单关联关系
            """
            sys_rel = [1, 2, 3, 4, 5, 6]
            for i, v in enumerate(sys_rel):
                if params_data['rid'] == str(v):
                    return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))
        model = TPermissionsResGroupRel()
        CRUDHelper.execute_delete_by_conditions(model, params_data)
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def get_resources_by_groupid():
        """
        通过用户组id获取资源列表
        :return:
        """
        params = request.values.get('params')
        params = json.loads(params)
        group_id = params['group_id']
        res_ids = PermissionsRelService.ids_in_groupids(
            model=TPermissionsResGroupRel(), gids=[group_id], select_column_name='rid')

        model = TPermissionsResource()
        conditions = dict(id=None, rule={})
        current_resources = None
        if res_ids:
            conditions['id'] = res_ids
            conditions['rule']['id'] = Constants.QUERY_CONDITION_RULE_IN
            current_resources = CRUDHelper.execute_select(model, conditions)
        return make_response(json.dumps(ResponseCode.response(data={"rows": current_resources}), ensure_ascii=False))

    @staticmethod
    def gen_resource_tree(resources):
        resource_tree = []
        root_pid = str(Constants.ROOT_PID)
        for i, item in enumerate(resources):
            if item['pid'] == root_pid:
                obj = dict()
                obj['id'] = item['id']
                obj['label'] = item['res_name']
                obj['desc'] = item['res_desc']
                obj['method'] = item['method']
                obj['uri'] = item['uri']
                obj['can_edit'] = item['can_edit']
                obj['disabled'] = False
                if item['can_edit'] == 'N':
                    obj['disabled'] = True
                resource_tree.append(obj)
        for i, item, in enumerate(resource_tree):
            PermissionsGroupService.recursion_resource_tree(item, resources)
        return resource_tree

    @staticmethod
    def recursion_resource_tree(current_resource, resources):
        """
        生成用户组资源树
        :param current_resource: 当前资源
        :param resources: 资源列表
        :return:
        """
        current_resource['children'] = []
        for i, item in enumerate(resources):
            if item['pid'] != current_resource['id']:
                continue
            else:
                obj = dict()
                obj['id'] = item['id']
                obj['label'] = item['res_name']
                obj['desc'] = item['res_desc']
                obj['method'] = item['method']
                obj['uri'] = item['uri']
                obj['can_edit'] = item['can_edit']
                obj['disabled'] = False
                if item['can_edit'] == 'N':
                    obj['disabled'] = True
                current_resource['children'].append(obj)
                # 递归
                PermissionsGroupService.recursion_resource_tree(obj, resources)
