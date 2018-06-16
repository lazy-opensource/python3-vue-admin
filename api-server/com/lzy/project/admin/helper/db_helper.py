#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/6 9:10
@file: db_helper.py
@desc: 获取db
"""
from flask_sqlalchemy import SQLAlchemy

from com.lzy.project.admin.exception.excepts import BlankParamExcept, NoneExcept
from com.lzy.project.admin.helper.sys_conf_helper import SysConfHelper
from com.lzy.project.admin.tools.log_util import info


class DbHelper:
    __db = SQLAlchemy()

    @staticmethod
    def init_db(app):
        if not app:
            raise (BlankParamExcept("app param is blank"))
        info('DbHelper', 'begin init database {0}'.format(SysConfHelper.get_item("mysql", "uri")))
        app.config['SQLALCHEMY_DATABASE_URI'] = SysConfHelper.get_item("mysql", "uri")
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        DbHelper.__db.init_app(app)

    @staticmethod
    def get_db():
        if not DbHelper.__db:
            raise (NoneExcept("db is none"))
        return DbHelper.__db
