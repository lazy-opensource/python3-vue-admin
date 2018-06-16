#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/12 13:50
@file: constant.py
@desc: 
"""


class Constants:
    # 有效数据
    VALID_STATUS_Y = 'Y'
    # 无效数据
    VALID_STATUS_N = 'N'
    # 超级管理员标示
    USER_TYPE_ADMIN = 'admin'
    # 普通用户标示
    USER_TYPE_COMMON = 'common'
    # 角色拥有资源的再分配权限
    AUTH_TYPE_AUTH = 'auth'
    # 角色没有资源的再分配权限
    AUTH_TYPE_NOT_AUTH = 'not_auth'
    # 资源类型 menu:菜单 f_uri:前台路由 a_uri:后台路由
    RES_TYPE_MENU = 'menu'
    RES_TYPE_URI = 'uri'
    # 导航栏菜单pid
    ROOT_PID = -1
    # 超级管理 ID
    ADMIN_ID = '1'
    # 查询条件规则
    QUERY_CONDITION_RULE_EQ = 'eq'
    QUERY_CONDITION_RULE_LIKE = 'like'
    QUERY_CONDITION_RULE_LE = 'le'
    QUERY_CONDITION_RULE_GE = 'ge'
    QUERY_CONDITION_RULE_IN = 'in'
