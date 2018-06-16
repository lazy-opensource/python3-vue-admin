#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/6 10:07
@file: basic.py
@desc: ORM实体父类
"""
from com.lzy.project.admin.helper.db_helper import DbHelper
from com.lzy.project.admin.tools.log_util import info


class BasicModel(object):
    __tablename__ = None
    id = DbHelper.get_db().Column(DbHelper.get_db().BigInteger(), primary_key=True)
    valid_status = DbHelper.get_db().Column(DbHelper.get_db().String(5), nullable=False, default='N')
    create_time = DbHelper.get_db().Column(DbHelper.get_db().DATETIME(), nullable=False)
    last_update_time = DbHelper.get_db().Column(DbHelper.get_db().DATETIME(), nullable=False)

    def get_table_name(self):
        return self.__tablename__

    def row_to_model(self, row):
        """
        通过数据库查出的行转换为Model
        :return:
        """
        attr_map = self.__dict__
        for k, v in attr_map.items():
            if k.startswith('_'):
                continue
            value = getattr(row, k)
            self.__setattr__(k, value)

    def to_json(self):
        """
        将对象属性装换为json
        :return: dict
        """
        attr_map = self.__dict__
        attr_json = {}
        for k, v in attr_map.items():
            if k.startswith('_'):
                continue
            value = getattr(self, k)
            attr_json[k] = str(value)
        return attr_json

    def set_attr_by_dist(self, dist):
        """
        根据给定的字典设置属性值
        :param dist: 字典
        :return: void
        """
        if not dist or len(dist.keys()) < 1:
            info("basic", "param dist is empty or null")
            return
        for k, v in dist.items():
            if v:
                setattr(self, k, v)


class BasicService(object):
    def callback(self, prefix, name, *args):
        """
        调用拼接函数，如果存在的话
        :param prefix: 函数前缀
        :param name:  函数名称
        :param args: 函数参数
        :return: 调用函数结果
        """
        method = getattr(self, prefix + name, None)
        if callable(method):
            return method(*args)
