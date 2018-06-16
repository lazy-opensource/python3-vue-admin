#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/13 8:51
@file: tests.py
@desc:
"""
from com.lzy.project.admin.model.t_permissions_model import TPermissionsGroup

model = TPermissionsGroup()
dist = {"group_name": "hello", "group_code": "world"}
model.set_attr_by_dist(dist)
print(model.to_json())
