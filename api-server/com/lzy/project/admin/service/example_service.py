#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/5 16:47
@file: t_example_model.py
@desc: 例子服务层
"""

from flask import request, make_response, json

from com.lzy.project.admin.base.basic import BasicService
from com.lzy.project.admin.helper.crud_helper import CRUDHelper
from com.lzy.project.admin.helper.db_helper import DbHelper
from com.lzy.project.admin.helper.sql_helper import SqlHelper
from com.lzy.project.admin.model.t_example_model import TExample
from com.lzy.project.admin.response.response import ResponseCode
from com.lzy.project.admin.tools.date_utils import DateUtils
from com.lzy.project.admin.tools.log_util import debug


class ExampleService(BasicService):
    single = None

    @classmethod
    def get_single(cls):
        """
        获取单实例
        :return:
        """
        if not cls.single:
            debug("exampleService", "实例化[exampleService]服务类")
            cls.single = ExampleService()
        return cls.single

    @staticmethod
    def hello():
        return "Hello World"

    @staticmethod
    def examples():
        """
        CRUD t_example表核心路由
        :return: json格式数据
        """
        method = request.method.lower()
        return ExampleService.get_single().callback("{0}_".format(method), "example")

    @staticmethod
    def put_example():
        """
        新增
        :return: json
        """
        params_data = request.get_json()['params']
        example = TExample()
        example.set_attr_by_dist(params_data)
        example.create_time = DateUtils.get_current_time()
        example.last_update_time = example.create_time
        DbHelper.get_db().session.add(example)
        DbHelper.get_db().session.commit()
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def post_example():
        """
        编辑
        :return: json
        """
        params_data = request.get_json()['params']
        params_data['last_update_time'] = DateUtils.get_current_time()
        DbHelper.get_db().session.query(TExample).filter_by(id=params_data['id']).update(params_data)
        DbHelper.get_db().session.commit()
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def delete_example():
        """
        删除
        :return: json
        """
        params_data = json.loads(request.args.get('ids'))
        DbHelper.get_db().session.execute(SqlHelper.gen_del_sql(TExample(), params_data))
        DbHelper.get_db().session.commit()
        return make_response(json.dumps(ResponseCode.response(), ensure_ascii=False))

    @staticmethod
    def get_example():
        """
        example 查询
        :return: json
        """
        params = request.values.get('params')
        conditions = json.loads(params)
        example_model = TExample()

        rows = CRUDHelper.execute_select(example_model, conditions)
        total = CRUDHelper.execute_select_count(example_model, conditions)
        data = {"total": total, "rows": rows}
        return make_response(json.dumps(ResponseCode.response(data=data), ensure_ascii=False))


if __name__ == '__main__':
    pass
