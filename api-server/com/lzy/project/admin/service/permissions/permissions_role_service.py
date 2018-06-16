#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/13 17:51
@file: permissions_role_service.py
@desc: 系统权限角色信息服务层
"""
from flask import request, json, make_response

from com.lzy.project.admin.base.basic import BasicService
from com.lzy.project.admin.constant.constant import Constants
from com.lzy.project.admin.helper.crud_helper import CRUDHelper
from com.lzy.project.admin.helper.db_helper import DbHelper
from com.lzy.project.admin.helper.sql_helper import SqlHelper
from com.lzy.project.admin.model.t_permissions_model import TPermissionsRole, TPermissionsRoleGroupRel, \
    TPermissionsUserRoleRel, TPermissionsResRoleRel, TPermissionsResGroupRel, TPermissionsResource
from com.lzy.project.admin.response.response import ResponseCode
from com.lzy.project.admin.service.permissions.permissions_rel_service import PermissionsRelService
from com.lzy.project.admin.service.permissions.permissions_resource_service import PermissionsResourceService
from com.lzy.project.admin.tools.date_utils import DateUtils
from com.lzy.project.admin.tools.log_util import debug


class PermissionsRoleService(BasicService):
    single = None

    @classmethod
    def get_single(cls):
        """
        获取单实例
        :return:
        """
        if not cls.single:
            debug("permissionsRoleService", "实例化[permissionsRoleService]服务类")
            cls.single = PermissionsRoleService()
        return cls.single

    @staticmethod
    def role_check_uniq():
        """
        检查唯一性约束
        :return: 结果对象
        """
        params = request.values.get('params')
        conditions = json.loads(params)
        model = TPermissionsRole()
        rows = CRUDHelper.execute_select(model=model, conditions=conditions)
        return make_response(json.dumps(ResponseCode.response(data=rows), ensure_ascii=False))

    @staticmethod
    def roles():
        """
        CRUD t_permissions_role表核心路由
        :return: json格式数据
        """
        method = request.method.lower()
        return PermissionsRoleService.get_single().callback("{0}_".format(method), "role")

    @staticmethod
    def get_role():
        """
        获取角色列表
        :return:
        """
        params = request.values.get('params')
        conditions = json.loads(params)

        model = TPermissionsRole()
        rows = CRUDHelper.execute_select(model, conditions)
        total = CRUDHelper.execute_select_count(model, conditions)
        DbHelper.get_db().session.close()
        data = {"total": total, "rows": rows}
        return make_response(json.dumps(ResponseCode.response(data=data), ensure_ascii=False))

    @staticmethod
    def put_role():
        """
        新增角色
        :return:
        """
        params_data = request.get_json()['params']
        role = TPermissionsRole()
        role.set_attr_by_dist(params_data)
        role.create_time = DateUtils.get_current_time()
        role.last_update_time = role.create_time
        DbHelper.get_db().session.add(role)
        DbHelper.get_db().session.commit()
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def post_role():
        """
        修改角色
        :return:
        """
        params_data = request.get_json()['params']
        params_data['last_update_time'] = DateUtils.get_current_time()
        DbHelper.get_db().session.query(TPermissionsRole).filter_by(id=params_data['id']).update(params_data)
        DbHelper.get_db().session.commit()
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def delete_role():
        """
        删除角色
        :return:
        """
        params_data = json.loads(request.args.get('ids'))
        if not params_data or len(params_data) < 1:
            raise Exception("参数 ids is blank")
        # 删除角色和用户组的关联关系
        PermissionsRelService.del_in_roleids(TPermissionsRoleGroupRel(), params_data)
        # 删除角色和用户的关联关系
        PermissionsRelService.del_in_roleids(TPermissionsUserRoleRel(), params_data)
        # 删除角色和资源的关联关系
        PermissionsRelService.del_in_roleids(TPermissionsResRoleRel(), params_data)
        CRUDHelper.execute_delete_by_field_in(TPermissionsRole(), params_data, 'id')
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def role_groups():
        """
        CRUD 角色关联的用户组数据
        :return: json格式数据
        """
        method = request.method.lower()
        return PermissionsRoleService.get_single().callback("{0}_".format(method), "role_group")

    @staticmethod
    def get_role_group():
        """
        获取角色关联的用户组数据
        :return:
        """
        params = request.values.get('params')
        params_data = json.loads(params)
        group_ids = PermissionsRelService.ids_in_roleids(TPermissionsRoleGroupRel(), [params_data['role_id']], 'gid')
        return make_response(json.dumps(ResponseCode.response(data=group_ids), ensure_ascii=False))

    @staticmethod
    def post_role_group():
        """
        更新角色和用户组的关联关系
        :return:
        """
        params_data = request.get_json()['params']
        role_id = params_data['role_id']
        group_ids = params_data['group_ids']
        if not role_id or len(role_id) < 1:
            raise Exception("参数 role_id is blank")
        # 删除角色和用户组的关联关系
        PermissionsRelService.del_in_roleids(TPermissionsRoleGroupRel(), [role_id])
        # 删除角色和用户的关联关系
        PermissionsRelService.del_in_roleids(TPermissionsUserRoleRel(), [role_id])
        # 删除角色和资源的关联关系
        PermissionsRelService.del_in_roleids(TPermissionsResRoleRel(), [role_id])
        # 重新关联
        if group_ids and len(group_ids) > 0:
            for group_id in group_ids:
                DbHelper.get_db().session.add(TPermissionsRoleGroupRel(
                    rid=role_id, gid=group_id, create_time=DateUtils.get_current_time(),
                    last_update_time=DateUtils.get_current_time()))
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def role_resources():
        """
        CRUD 角色关联的资源数据
        :return: json格式数据
        """
        method = request.method.lower()
        return PermissionsRoleService.get_single().callback("{0}_".format(method), "role_resource")

    @staticmethod
    def get_role_resource():
        """
        根据角色获取资源
        可以关联的资源    已经关联的资源
        :return:
        """
        params = request.values.get('params')
        params_data = json.loads(params)
        role_id = params_data['role_id']
        if not role_id:
            raise Exception('param role_id is blank')
        response_data = {'all_can_rel_rows': [], 'aleary_rel_rows': []}
        group_ids = PermissionsRelService.ids_in_roleids(TPermissionsRoleGroupRel(), [role_id], 'gid')
        if not group_ids or len(group_ids) < 1:
            return make_response(json.dumps(ResponseCode.response(data=response_data), ensure_ascii=False))
        all_can_rel_resource_ids = PermissionsRelService.ids_in_groupids(TPermissionsResGroupRel(), group_ids, 'rid')
        if not all_can_rel_resource_ids or len(all_can_rel_resource_ids) < 1:
            return make_response(json.dumps(ResponseCode.response(data=response_data), ensure_ascii=False))
        all_aleary_rel_res_ids = PermissionsRelService.ids_in_roleids(TPermissionsResRoleRel(), [role_id], 'res_id')
        response_data['all_can_rel_rows'] = PermissionsResourceService. \
            gen_resource_tree(CRUDHelper.execute_select(TPermissionsResource(), {'id': all_can_rel_resource_ids, 'rule': {
             'id': Constants.QUERY_CONDITION_RULE_IN}}))
        response_data['aleary_rel_rows'] = all_aleary_rel_res_ids
        return make_response(json.dumps(ResponseCode.response(data=response_data), ensure_ascii=False))

    @staticmethod
    def post_role_resource():
        """
        重新关联资源
        :return:
        """
        params_data = request.get_json()['params']
        role_id = params_data['role_id']
        res_ids = params_data['res_ids']
        if not role_id:
            raise Exception('param role_id is none')
        PermissionsRelService.del_in_roleids(model=TPermissionsResRoleRel(), rids=[role_id])
        for i, rid in enumerate(res_ids):
            DbHelper.get_db().session.add(TPermissionsResRoleRel(
                res_id=rid, role_id=role_id,
                valid_status=Constants.VALID_STATUS_Y,
                create_time=DateUtils.get_current_time(),
                last_update_time=DateUtils.get_current_time()))
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))
