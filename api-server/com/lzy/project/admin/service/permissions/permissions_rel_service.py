#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/13 18:12
@file: permissions_rel_service.py
@desc: 系统权限多对多关联关系服务层
"""
from com.lzy.project.admin.base.basic import BasicService
from com.lzy.project.admin.constant.constant import Constants
from com.lzy.project.admin.helper.crud_helper import CRUDHelper
from com.lzy.project.admin.helper.db_helper import DbHelper
from com.lzy.project.admin.model.t_permissions_model import TPermissionsResRoleRel


class PermissionsRelService(BasicService):

    @staticmethod
    def __filter_ids(rows, id_name):
        """
        过滤其它字段，只取id属性
        :param rows: 结果集
        :return: 过滤后的id列表
        """
        ids = []
        for i, item in enumerate(rows):
            ids.append(item[id_name])
        return ids

    @staticmethod
    def ids_by_userid(model, uid, select_column_name, valid_status=Constants.VALID_STATUS_Y):
        """
        通过用户id获取角色、组id列表
        :param select_column_name:
        :param valid_status: 数据有效状态
        :param uid: 用户id
        :param model: 表模型
        :return: 角色、组id列表
        """
        conditions = {"uid": uid, "valid_status": valid_status}
        rows = CRUDHelper.execute_select(model, conditions)
        return PermissionsRelService.__filter_ids(rows, select_column_name)

    @staticmethod
    def ids_in_roleids(model, rids, select_column_name, valid_status=Constants.VALID_STATUS_Y):
        """
        通过角色ids获取资源、组id列表
        :param select_column_name:
        :param valid_status: 数据有效状态
        :param rids: 角色ids
        :param model: 表模型
        :return: 资源、组id列表
        """
        role_id_name = 'rid'
        if isinstance(model, TPermissionsResRoleRel):
            role_id_name = 'role_id'
        conditions = {role_id_name: rids, "valid_status": valid_status, "rule": {role_id_name: "in"}}
        rows = CRUDHelper.execute_select(model, conditions)
        return PermissionsRelService.__filter_ids(rows, select_column_name)

    @staticmethod
    def ids_in_groupids(model, gids, select_column_name, valid_status=Constants.VALID_STATUS_Y):
        """
        通过用户组ids查资源/角色id列表
        :param select_column_name:
        :param valid_status: 数据有效状态
        :param model: 表模型
        :param gids: 组id列表
        :return: 资源/角色id列表
        """
        conditions = {"gid": gids, "valid_status": valid_status, "rule": {"gid": "in"}}
        rows = CRUDHelper.execute_select(model, conditions)
        return PermissionsRelService.__filter_ids(rows, select_column_name)

    @staticmethod
    def del_in_roleids(model, rids):
        """
        删除给定的角色id列表相关的关联数据
        :param model: 表模型
        :param rids: 角色ids
        :return: void
        """
        role_id_name = 'rid'
        if isinstance(model, TPermissionsResRoleRel):
            role_id_name = 'role_id'
        # 角色和用户的关联关系
        # 角色和资源的关联关系
        # 角色和用户组的关联关系
        CRUDHelper.execute_delete_by_field_in(model, rids, field_name=role_id_name)

    @staticmethod
    def del_in_uids(model, uids):
        """
        删除给定的用户id列表相关的关联数据
        :param model: 表模型
        :param uids: 用户ids
        :return: void
        """
        # 用户和角色的关联关系
        # 用户和用户组的关联关系
        CRUDHelper.execute_delete_by_field_in(model, uids, field_name='uid')

    @staticmethod
    def del_in_groupids(model, groupids):
        """
        删除给定的用户组id列表相关的关联数据
        :param model: 表模型
        :param groupids: 用户组ids
        :return: void
        """
        # 用户组和角色的关联关系
        # 用户和用户组的关联关系
        # 用户组和资源的关联关系
        CRUDHelper.execute_delete_by_field_in(model, groupids, field_name='gid')

    @staticmethod
    def upd_in_ids(model, kv, ids):
        CRUDHelper.execute_upd(model, kv, ids)

    @staticmethod
    def del_in_resids(model, rids):
        """
        删除给定的资源id列表相关的关联数据
        :param model: 表模型
        :param rids: 资源ids
        :return:
        """
        id_name = 'rid'
        if isinstance(model, TPermissionsResRoleRel):
            id_name = 'res_id'
        # 资源和用户组的关联关系
        # 资源和角色的关联关系
        CRUDHelper.execute_delete_by_field_in(model, rids, field_name=id_name)

    @staticmethod
    def insert_relations(models):
        """
        批量插入关联关系
        :param models: 关联关系模型列表
        :return: void
        """
        for i, model in enumerate(models):
            DbHelper.get_db().session.add(model)
        DbHelper.get_db().session.commit()

    @staticmethod
    def del_relation(models):
        """
        批量删除关联关系
        :param models: 关联关系模型列表
        :return:
        """
        for i, model in enumerate(models):
            DbHelper.get_db().session.delete(model)
        DbHelper.get_db().session.commit()
