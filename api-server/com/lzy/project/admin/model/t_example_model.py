#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: LaiZHiYuan
@time: 2018/3/5 16:47
@file: t_example_model.py
@desc: t_example table model
"""

from com.lzy.project.admin.base.basic import BasicModel
from com.lzy.project.admin.helper.db_helper import DbHelper
from com.lzy.project.admin.tools.date_utils import DateUtils


class TExample(DbHelper.get_db().Model, BasicModel):
    __tablename__ = 't_example'
    name = DbHelper.get_db().Column(DbHelper.get_db().String(30))
    age = DbHelper.get_db().Column(DbHelper.get_db().Integer())
    email = DbHelper.get_db().Column(DbHelper.get_db().String(30))

    def __init__(self, id=None, name=None, age=None, email=None, valid_status=None, create_time=None,
                 last_update_time=None):
        self.id = id
        self.name = name
        self.age = age
        self.email = email
        self.valid_status = valid_status
        self.create_time = create_time
        self.last_update_time = last_update_time

    # def to_json(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "age": self.age,
    #         "email": self.email,
    #         "valid_status": self.valid_status,
    #         "create_time": self.create_time,
    #         "last_update_time": self.last_update_time
    #     }


def init_test_data():
    from flask import Flask
    app = Flask(__name__)
    DbHelper.init_db(app)
    app.app_context().push()
    DbHelper.get_db().create_all()

    example = TExample()
    example.age = "29"
    example.email = '10594463@qq.com'
    example.name = 'lisi'
    example.create_time = DateUtils.get_current_time()
    example.last_update_time = example.create_time

    example5 = TExample()
    example5.age = 25
    example5.email = '10594463@qq.com'
    example5.name = 'lisi'
    example5.create_time = DateUtils.get_current_time()
    example5.last_update_time = example.create_time

    example4 = TExample()
    example4.age = "26"
    example4.email = '10594463@qq.com'
    example4.name = 'wangwu'
    example4.create_time = DateUtils.get_current_time()
    example4.last_update_time = example.create_time

    example3 = TExample()
    example3.age = "32"
    example3.email = '1059477777463@qq.com'
    example3.name = 'zhaoliu'
    example3.create_time = DateUtils.get_current_time()
    example3.last_update_time = example.create_time

    example2 = TExample()
    example2.age = "21"
    example2.email = '7866510594463@qq.com'
    example2.name = 'chenghai'
    example2.create_time = DateUtils.get_current_time()
    example2.last_update_time = example.create_time

    example1 = TExample()
    example1.age = 38
    example1.email = '16566760594463@qq.com'
    example1.name = 'chengxi'
    example1.create_time = DateUtils.get_current_time()
    example1.last_update_time = example.create_time
    DbHelper.get_db().session.add(example)
    DbHelper.get_db().session.add(example1)
    DbHelper.get_db().session.add(example2)
    DbHelper.get_db().session.add(example3)
    DbHelper.get_db().session.add(example4)
    DbHelper.get_db().session.add(example5)
    DbHelper.get_db().session.commit()


def test_crud():
    from flask import Flask

    app = Flask(__name__)
    DbHelper.init_db(app)
    app.app_context().push()
    example = TExample.query.filter_by(name='lisi').first()
    print(str(example))

    # print(json.dumps(example, ensure_ascii=False))


def test_getarr():
    attrs = TExample().__dict__
    del attrs['_sa_instance_state']
    print(attrs)


def test_to_json():
    example = TExample()
    example.id = 123456
    example.name = 'zhangsan'
    example.age = 25
    example.last_update_time = DateUtils.get_current_time()
    example.create_time = example.last_update_time
    print(example.to_json())


if __name__ == '__main__':
    init_test_data()
    # test_crud()
    # print(TExample().get_table_name())
    # test_getarr()
    # test_to_json()
