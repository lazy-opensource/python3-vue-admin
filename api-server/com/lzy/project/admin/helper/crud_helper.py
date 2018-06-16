#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/14 16:38
@file: crud_helper.py
@desc: 是实现增删查改封装类
"""
from com.lzy.project.admin.helper.db_helper import DbHelper
from com.lzy.project.admin.helper.sql_helper import SqlHelper, Rule
from com.lzy.project.admin.tools.log_util import info


class CRUDHelper:

    @staticmethod
    def execute_upd(model, fv, ids):
        sql = 'update {0} '.format(model.get_table_name())
        for k, v in fv.items():
            if v:
                sql += " set {0}='{1}',".format(k, v)
        sql = sql[:-1]
        sql += ' where 1=1 ' + Rule.rule_in('id', ids)
        info('curdHelper', 'update sql:' + sql)
        DbHelper.get_db().session.execute(sql)

    @staticmethod
    def execute_select(model, conditions):
        result_set = DbHelper.get_db().session.execute(
            SqlHelper.gen_select_sql(model.get_table_name(), conditions)).fetchall()
        rows = []
        fields = model.__dict__
        for i, row in enumerate(result_set):
            obj = {}
            for j, field in enumerate(fields):
                if field in row.keys():
                    obj[field] = str(row[field])
            rows.append(obj)
        return rows

    @staticmethod
    def execute_select_count(model, conditions):
        result_set = DbHelper.get_db().session.execute(
            SqlHelper.gen_select_sql(model.get_table_name(), conditions, True)).first()
        return result_set[0] if result_set else 0

    @staticmethod
    def execute_delete_by_field_in(model, value_in_list, field_name='id'):
        DbHelper.get_db().session.execute(SqlHelper.gen_del_sql(model, value_in_list, field_name=field_name))

    @staticmethod
    def execute_delete_by_conditions(model, conditions):
        DbHelper.get_db().session.execute(SqlHelper.gen_condition_del_sql(model.get_table_name(), conditions))
