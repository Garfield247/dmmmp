#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from flask import jsonify
from flask_script import Manager, Server
from flask_migrate import MigrateCommand

from dmp import app
from dmp.extensions import db

# 创建命令起动控制对象
manager = Manager(app)
# 添加数据库迁移命令
manager.add_command('db', MigrateCommand)
# 添加服务配置


manager.add_command('runserver', Server(host='0.0.0.0', port=7789))


# 路由列表命令
@manager.command
def url_map():
    for i in app.url_map.__dict__.get("_rules"):
        app.logger.info(i)


# 删除所有表
@manager.command
def drop_db():
    app.logger.info("drop db")
    db.drop_all()


# 创建所有表
@manager.command
def create_db():
    app.logger.info("create db")
    db.create_all()


# 生成数据表测试数据
@manager.command
def create_test_db_table_data():
    import random
    from dmp.models import Users, Case, Database
    from dmp.api.dbtable import post
    count = 30
    for i in range(count):
        new_test_table = post(
            dmp_data_table_name="dmp_test_dbtable_%d" % i,
            db_table_name="dmp_test_db_table_name%d" % i,
            description="测试表",
            dmp_user_id=random.choice(Users.query.all()).id,
            dmp_database_id=random.choice(Database.query.all()).id,
            dmp_case_id=random.choice(Case.query.all()).id
        )

        app.logger.info("add test data :" + str(new_test_table))

        app.logger.info("add test data :" + str(new_test_table))


# 初始化
@manager.command
def sys_init():
    db.drop_all()
    db.create_all()
    from dmp.models import Permissions
    Permissions.init_permission()
    from dmp.models import Groups
    Groups.init_group()
    from dmp.models import Users
    Users.create_test_user()


@manager.option('-n', '-dmp_username', dest='dmp_username')
@manager.option('-r', '-real_name', dest='real_name')
@manager.option('-p', '-passwd', dest='passwd')
@manager.option('-e', '-email', dest='email')
def createsuperuser(dmp_username, real_name, passwd, email):
    """创建管理员用户"""
    from dmp.models import Users, Groups
    from dmp.utils.ep_data import EnvelopedData
    if not all([dmp_username, real_name, passwd, email]):
        return jsonify({
            'status': -1,
            'msg': 'Insufficient parameter, please recreate superuser',
            'results': {}
        })

    db_user_count = Users.query.count()
    print('00---', db_user_count)
    # user_root_list = Users.query.filter(Users.dmp_group_id == 1).all()
    if db_user_count == 0:
        user = Users(dmp_username=dmp_username, real_name=real_name, password=passwd, email=email)
        rootgroup = Groups.query.filter(Groups.id == 1).first()
        user.dmp_group_id = 1
        user.leader_dmp_user_id = None
        res = EnvelopedData.create_root(rootgroup, user, email)
        if isinstance(res, str):
            return {'msg': res}
        return {'msg': 'The email of the register root has been sent, please click activate'}
    else:
        return {'msg': 'The super administrator already exists in the database, please do not add it again'}
    # except Exception:
    #     return {'msg': 'Other error.'}

    # try:
    #     user = Users(dmp_username=dmp_username, real_name=real_name, password=passwd, email=email)
    #     user.dmp_group_id = 1
    #     user_root_list = Users.query.filter(Users.dmp_group_id == 1).all()
    #     rootgroup = Groups.query.filter(Groups.dmp_group_name == "root").first()
    #
    #     # 管理员数量达到最大容量
    #     if len(user_root_list) == rootgroup.max_count == 3:
    #         return {'msg': 'The maximum number of administrators has been reached'}
    #
    #     # 第一个创建的管理员为超级管理员--leader_dmp_user_id = None
    #     elif len(user_root_list) == 0 and rootgroup.max_count == None:
    #         try:
    #             user.leader_dmp_user_id = None
    #             res = EnvelopedData.create_root(rootgroup, user, email)
    #             if isinstance(res, str):
    #                 return {'msg': res}
    #             return {'msg': 'The email of the register root has been sent, please click activate'}
    #         except Exception:
    #             return {'msg': 'Other error.'}
    #
    #     # 创建管理员--最多创建2个
    #     elif len(user_root_list) == rootgroup.max_count and rootgroup.max_count <= 3 and rootgroup.max_count != None:
    #         try:
    #             user.leader_dmp_user_id = 1
    #             res = EnvelopedData.create_root(rootgroup, user, email)
    #             if isinstance(res, str):
    #                 return {'msg': res}
    #             return {'msg': 'The email of the register root has been sent, please click activate'}
    #         except Exception:
    #             return {'msg': 'Other error.'}
    #
    #     # 管理员数量和管理员用户组容量数不对应
    #     elif len(user_root_list) != rootgroup.max_count:
    #         return {'msg': 'The data has been tampered with, please contact the administrator to view and fix it'}
    # # 其他错误
    # except Exception as err:
    #     return {'msg': err}


if __name__ == '__main__':
    manager.run()
