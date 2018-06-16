#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/13 17:58
@file: permissions_resource_service.py
@desc: 系统权限资源信息服务层
"""
from flask import request, json, make_response

from com.lzy.project.admin.base.basic import BasicService
from com.lzy.project.admin.constant.constant import Constants
from com.lzy.project.admin.helper.crud_helper import CRUDHelper
from com.lzy.project.admin.helper.db_helper import DbHelper
from com.lzy.project.admin.helper.sql_helper import SqlHelper
from com.lzy.project.admin.model.t_permissions_model import TPermissionsResource, TPermissionsUserRoleRel, \
    TPermissionsResRoleRel, TPermissionsResGroupRel, TPermissionsUserGroupRel
from com.lzy.project.admin.response.response import ResponseCode
from com.lzy.project.admin.service.permissions.permissions_rel_service import PermissionsRelService
from com.lzy.project.admin.tools.date_utils import DateUtils
from com.lzy.project.admin.tools.log_util import debug


class PermissionsResourceService(BasicService):
    single = None

    @classmethod
    def get_single(cls):
        """
        获取单实例
        :return:
        """
        if not cls.single:
            debug("permissionsResourceService", "实例化[permissionsResourceService]服务类")
            cls.single = PermissionsResourceService()
        return cls.single

    @staticmethod
    def resource_check_uniq():
        """
        检查唯一性约束
        :return: 结果对象
        """
        params = request.values.get('params')
        conditions = json.loads(params)
        model = TPermissionsResource()
        rows = CRUDHelper.execute_select(model=model, conditions=conditions)
        return make_response(json.dumps(ResponseCode.response(data=rows), ensure_ascii=False))

    @staticmethod
    def resource_by_id():
        """
        根据id获取数据
        :return: json格式数据
        """
        res_id = request.values.get('res_id')
        if res_id:
            row = TPermissionsResource.query.get(res_id)
            model = TPermissionsResource()
            model.row_to_model(row)
            return make_response(json.dumps(ResponseCode.response(data=model.to_json()),
                                            ensure_ascii=False))
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def resources():
        """
        CRUD t_permissions_resource表核心路由
        :return: json格式数据
        """
        method = request.method.lower()
        return PermissionsResourceService.get_single().callback("{0}_".format(method), "resource")

    @staticmethod
    def get_resource():
        """
        获取权限资源列表
        :return:
        """
        model = TPermissionsResource()
        rows = CRUDHelper.execute_select(model, {})
        data = {"rows": PermissionsResourceService.gen_resource_tree(rows)}
        return make_response(json.dumps(ResponseCode.response(data=data), ensure_ascii=False))

    @staticmethod
    def gen_resource_tree(resources):
        """
        生成资源树
        :param resources: 资源结果集
        :return:
        """
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
            PermissionsResourceService.recursion_resource_tree(item, resources)
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
                PermissionsResourceService.recursion_resource_tree(obj, resources)

    @staticmethod
    def put_resource():
        """
        新增权限资源
        :return:
        """
        params_data = request.get_json()['params']
        params_data['pid'] = params_data['pid'] if params_data['pid'] else Constants.ROOT_PID

        resource = TPermissionsResource()
        resource.set_attr_by_dist(params_data)
        resource.create_time = DateUtils.get_current_time()
        resource.last_update_time = resource.create_time
        DbHelper.get_db().session.add(resource)
        DbHelper.get_db().session.commit()
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def post_resource():
        """
        修改权限资源
        :return:
        """
        params_data = request.get_json()['params']
        params_data['last_update_time'] = DateUtils.get_current_time()
        DbHelper.get_db().session.query(TPermissionsResource).filter_by(id=params_data['id']).update(params_data)
        DbHelper.get_db().session.commit()
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def delete_resource():
        """
        删除权限资源
        :return:
        """
        params_data = json.loads(request.args.get('ids'))
        if len(params_data) > 0:
            # 删除资源和用户组的关联关系
            PermissionsRelService.del_in_resids(TPermissionsResGroupRel(), params_data)
            # 删除角色和资源的关联关系
            PermissionsRelService.del_in_resids(TPermissionsResRoleRel(), params_data)
            CRUDHelper.execute_delete_by_field_in(TPermissionsResource(), params_data, 'id')
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def resources_by_user(uid, res_type, pid=Constants.ROOT_PID, valid_status=Constants.VALID_STATUS_Y):
        """
        通过用户id、用户类型、资源类型查资源列表（导航菜单，前台uri，后台uri）
        :param valid_status:
        :param pid: 父级id
        :param res_type: 资源类型
        :param uid: 用户id
        :return:
        """
        # 根据用户查所属的用户组
        group_ids = PermissionsRelService.ids_by_userid(TPermissionsUserGroupRel(), uid, "gid")
        if not group_ids or len(group_ids) < 1:
            return []
        # 获取用户所在的所有用户组的权限数据
        group_res_ids = PermissionsRelService.ids_in_groupids(TPermissionsResGroupRel(), group_ids, "rid")
        if not group_res_ids or len(group_res_ids) < 1:
            return []
        # 根据用户查角色ids
        role_ids = PermissionsRelService.ids_by_userid(model=TPermissionsUserRoleRel(),
                                                             uid=uid, select_column_name='rid') if uid else []
        if not role_ids or len(role_ids) < 1:
            return []
        # 根据角色查资源ids
        role_res_ids = PermissionsRelService.ids_in_roleids(TPermissionsResRoleRel(), role_ids, 'res_id')
        if not role_res_ids or len(role_res_ids) < 1:
            return []

        # 计算用户组资源集合和角色资源集合的交集得到最终用户的所有资源id
        user_res_ids = list(set(group_res_ids).intersection(set(role_res_ids)))

        # 创建查找条件
        conditions = {
            "id": user_res_ids,
            "res_type": res_type,
            "valid_status": valid_status
        }
        # 菜单资源时才有根据父查子数据
        if pid and res_type == Constants.RES_TYPE_MENU:
            conditions['pid'] = pid

        conditions['rule'] = {"id": Constants.QUERY_CONDITION_RULE_IN}
        rows = CRUDHelper.execute_select(TPermissionsResource(), conditions)
        return rows

    @staticmethod
    def get_permission():
        """
        根据用户id、用户类型获取资源api
        :return:
        """
        params = request.values.get('params')
        params = json.loads(params)
        uid = params['uid']
        # 权限资源
        # 导航菜单
        nav_menus = PermissionsResourceService.resources_by_user(uid=uid, res_type=Constants.RES_TYPE_MENU)
        # 前台路由
        # f_uris = PermissionsResourceService.resources_by_user(uid=uid,
        #                                                    user_type=utype, res_type=Constants.RES_TYPE_FURI)
        # 后台路由
        a_uris = PermissionsResourceService.resources_by_user(uid=uid, res_type=Constants.RES_TYPE_AURI)
        data = dict(nav_menus=nav_menus, a_uris=a_uris)
        data['nav_menus'] = json.dumps(nav_menus)
        # data['f_uris'] = json.dumps(f_uris)
        data['a_uris'] = json.dumps(a_uris)
        data['upd_resource_time'] = DateUtils.get_current_time()
        return make_response(
            json.dumps(ResponseCode.response(data=data), ensure_ascii=False))

    @staticmethod
    def get_permission_submenus():
        params = request.values.get('params')
        params = json.loads(params)
        pid = params['pid']
        uid = params['uid']
        submenus = PermissionsResourceService.resources_by_user(
            uid=uid, res_type=Constants.RES_TYPE_MENU, pid=None)
        # 没有子菜单
        if not submenus or len(submenus) < 1:
            return make_response(
                json.dumps(ResponseCode.response(data=[]), ensure_ascii=False))
        one_submenus_by_pid = []
        # 从所有的子菜单中找出该pid下的一级子菜单
        for i, item in enumerate(submenus):
            if item['pid'] == pid:
                one_submenus_by_pid.append(item)
        # 递归遍历出一级子菜单的子菜单
        for i, item in enumerate(one_submenus_by_pid):
            PermissionsResourceService.gen_submenu_tree(item, submenus)
        return make_response(
            json.dumps(ResponseCode.response(data=one_submenus_by_pid), ensure_ascii=False))

    @staticmethod
    def gen_submenu_tree(current_menu, menus):
        """
        生成菜单树p
        :param current_menu:
        :param menus:
        :return:
        """
        current_menu['submenus'] = []
        for i, item in enumerate(menus):
            if item['pid'] != current_menu['id']:
                continue
            else:
                current_menu['submenus'].append(item)
                # 递归
                PermissionsResourceService.gen_submenu_tree(item, menus)
