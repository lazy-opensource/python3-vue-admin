#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/5 16:47
@file: t_permissions_model.py
@desc: 系统权限表模型
"""
from werkzeug.security import generate_password_hash, check_password_hash

from com.lzy.project.admin.base.basic import BasicModel
from com.lzy.project.admin.helper.db_helper import DbHelper


class TPermissionsUser(DbHelper.get_db().Model, BasicModel):
    """
    系统权限用户表模型
    """
    __tablename__ = 't_permissions_user'
    nickname = DbHelper.get_db().Column(DbHelper.get_db().String(50), nullable=False)
    password = DbHelper.get_db().Column(DbHelper.get_db().String(50), nullable=False)
    salt = DbHelper.get_db().Column(DbHelper.get_db().String(40), nullable=False)
    login_name = DbHelper.get_db().Column(DbHelper.get_db().String(60), nullable=False)
    contact = DbHelper.get_db().Column(DbHelper.get_db().String(11), nullable=False)
    can_edit = DbHelper.get_db().Column(DbHelper.get_db().String(5), nullable=False)

    def __init__(self, id=None, nickname=None, password=None,
                 salt=None, login_name=None, contact=None,
                 valid_status='Y', create_time=None, last_update_time=None, can_edit='Y'):
        self.can_edit = can_edit
        self.id = id
        self.nickname = nickname
        self.password = password
        if self.password:
            self.password = generate_password_hash(password)
        self.salt = salt
        self.login_name = login_name
        self.contact = contact
        self.valid_status = valid_status
        self.create_time = create_time
        self.last_update_time = last_update_time

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)


class TPermissionsRole(DbHelper.get_db().Model, BasicModel):
    """
    系统权限角色表模型
    """
    __tablename__ = 't_permissions_role'
    pid = DbHelper.get_db().Column(DbHelper.get_db().BigInteger(), nullable=False)
    role_name = DbHelper.get_db().Column(DbHelper.get_db().String(30), nullable=False)
    role_code = DbHelper.get_db().Column(DbHelper.get_db().String(40), nullable=False)
    can_edit = DbHelper.get_db().Column(DbHelper.get_db().String(5), nullable=False)

    def __init__(self, id=None, valid_status='Y',
                 create_time=None, last_update_time=None,
                 pid=None, role_name=None, role_code=None, can_edit='Y'):
        self.can_edit = can_edit
        self.id = id
        self.valid_status = valid_status
        self.create_time = create_time
        self.last_update_time = last_update_time
        self.pid = pid
        self.role_code = role_code
        self.role_name = role_name


class TPermissionsResource(DbHelper.get_db().Model, BasicModel):
    """
    系统权限资源表模型
    """
    __tablename__ = 't_permissions_resource'
    res_name = DbHelper.get_db().Column(DbHelper.get_db().String(50), nullable=False)
    res_desc = DbHelper.get_db().Column(DbHelper.get_db().String(50), nullable=False)
    res_code = DbHelper.get_db().Column(DbHelper.get_db().String(50), nullable=False)
    pid = DbHelper.get_db().Column(DbHelper.get_db().BigInteger(), nullable=False)
    icon = DbHelper.get_db().Column(DbHelper.get_db().String(50), nullable=False)
    method = DbHelper.get_db().Column(DbHelper.get_db().String(10), nullable=False)
    res_order = DbHelper.get_db().Column(DbHelper.get_db().Integer(), nullable=False)
    uri = DbHelper.get_db().Column(DbHelper.get_db().String(100), nullable=False)
    res_type = DbHelper.get_db().Column(DbHelper.get_db().String(20), nullable=False)
    can_edit = DbHelper.get_db().Column(DbHelper.get_db().String(5), nullable=False)

    def __init__(self, id=None, valid_status='Y', create_time=None, last_update_time=None, res_code=None,
                 pid=None, method='', res_order=100, res_name=None, res_desc=None, icon='el-icon-menu', uri='',
                 res_type=None, can_edit='Y'):
        self.can_edit = can_edit
        self.id = id
        self.method = method
        self.res_order = res_order
        self.valid_status = valid_status
        self.create_time = create_time
        self.last_update_time = last_update_time
        self.pid = pid
        self.res_name = res_name
        self.res_desc = res_desc
        self.res_code = res_code
        self.icon = icon
        self.uri = uri
        self.res_type = res_type


class TPermissionsGroup(DbHelper.get_db().Model, BasicModel):
    """
    系统权限用户组表模型
    """
    __tablename__ = 't_permissions_group'
    pid = DbHelper.get_db().Column(DbHelper.get_db().BigInteger(), nullable=False)
    group_name = DbHelper.get_db().Column(DbHelper.get_db().String(30), nullable=False)
    group_desc = DbHelper.get_db().Column(DbHelper.get_db().String(40), nullable=False)
    group_code = DbHelper.get_db().Column(DbHelper.get_db().String(40), nullable=False)
    can_edit = DbHelper.get_db().Column(DbHelper.get_db().String(5), nullable=False)

    def __init__(self, id=None, valid_status='Y', create_time=None, group_code=None,
                 last_update_time=None, pid=None, group_name=None, group_desc=None, can_edit='Y'):
        self.can_edit = can_edit
        self.id = id
        self.valid_status = valid_status
        self.create_time = create_time
        self.last_update_time = last_update_time
        self.pid = pid
        self.group_desc = group_desc
        self.group_code = group_code
        self.group_name = group_name


class TPermissionsUserRoleRel(DbHelper.get_db().Model, BasicModel):
    """
    系统权限用户和角色多对多关系表模型
    """
    __tablename__ = 't_permissions_user_role_rel'
    uid = DbHelper.get_db().Column(DbHelper.get_db().BigInteger(), nullable=False)
    rid = DbHelper.get_db().Column(DbHelper.get_db().BigInteger(), nullable=False)
    can_edit = DbHelper.get_db().Column(DbHelper.get_db().String(5), nullable=False)

    def __init__(self, id=None, valid_status='Y', create_time=None, last_update_time=None, uid=None, rid=None,
                 can_edit='Y'):
        self.can_edit = can_edit
        self.id = id
        self.valid_status = valid_status
        self.create_time = create_time
        self.last_update_time = last_update_time
        self.rid = rid
        self.uid = uid


class TPermissionsResRoleRel(DbHelper.get_db().Model, BasicModel):
    """
    系统权限资源和角色多对多关系表模型
    """
    __tablename__ = 't_permissions_res_role_rel'
    role_id = DbHelper.get_db().Column(DbHelper.get_db().BigInteger(), nullable=False)
    res_id = DbHelper.get_db().Column(DbHelper.get_db().BigInteger(), nullable=False)
    auth_type = DbHelper.get_db().Column(DbHelper.get_db().String(10), nullable=False)
    can_edit = DbHelper.get_db().Column(DbHelper.get_db().String(5), nullable=False)

    def __init__(self, id=None, auth_type='CAN', valid_status='Y', create_time=None,
                 last_update_time=None, role_id=None, res_id=None, can_edit='Y'):
        self.can_edit = can_edit
        self.id = id
        self.valid_status = valid_status
        self.create_time = create_time
        self.last_update_time = last_update_time
        self.role_id = role_id
        self.res_id = res_id
        self.auth_type = auth_type


class TPermissionsUserGroupRel(DbHelper.get_db().Model, BasicModel):
    """
     系统权限用户和用户组多对多关系表模型
    """
    __tablename__ = 't_permissions_user_group_rel'
    uid = DbHelper.get_db().Column(DbHelper.get_db().BigInteger(), nullable=False)
    gid = DbHelper.get_db().Column(DbHelper.get_db().BigInteger(), nullable=False)
    can_edit = DbHelper.get_db().Column(DbHelper.get_db().String(5), nullable=False)

    def __init__(self, id=None, valid_status='Y',
                 create_time=None, last_update_time=None, uid=None, gid=None, can_edit='Y'):
        self.can_edit = can_edit
        self.id = id
        self.valid_status = valid_status
        self.create_time = create_time
        self.last_update_time = last_update_time
        self.gid = gid
        self.uid = uid


class TPermissionsRoleGroupRel(DbHelper.get_db().Model, BasicModel):
    """
    系统权限角色和用户组多对多关系表模型
    """
    __tablename__ = 't_permissions_role_group_rel'
    rid = DbHelper.get_db().Column(DbHelper.get_db().BigInteger(), nullable=False)
    gid = DbHelper.get_db().Column(DbHelper.get_db().BigInteger(), nullable=False)
    can_edit = DbHelper.get_db().Column(DbHelper.get_db().String(5), nullable=False)

    def __init__(self, id=None, valid_status='Y', create_time=None, last_update_time=None, rid=None, gid=None,
                 can_edit='Y'):
        self.can_edit = can_edit
        self.id = id
        self.valid_status = valid_status
        self.create_time = create_time
        self.last_update_time = last_update_time
        self.gid = gid
        self.rid = rid


class TPermissionsResGroupRel(DbHelper.get_db().Model, BasicModel):
    """
    系统权限资源和用户组多对多关系表模型
    """
    __tablename__ = 't_permissions_res_group_rel'
    rid = DbHelper.get_db().Column(DbHelper.get_db().BigInteger(), nullable=False)
    gid = DbHelper.get_db().Column(DbHelper.get_db().BigInteger(), nullable=False)
    can_edit = DbHelper.get_db().Column(DbHelper.get_db().String(5), nullable=False)

    def __init__(self, id=None, valid_status='Y', create_time=None, last_update_time=None, rid=None, gid=None,
                 can_edit='Y'):
        self.can_edit = can_edit
        self.id = id
        self.valid_status = valid_status
        self.create_time = create_time
        self.last_update_time = last_update_time
        self.gid = gid
        self.rid = rid
