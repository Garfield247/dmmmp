#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD


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


@manager.command
def test_datax():
    from dmp.test.datax_test import test
    test()

    # from dmp.models import Users
    # Users.create_test_user()


@manager.option('-n', '-dmp_username', dest='dmp_username')
@manager.option('-r', '-real_name', dest='real_name')
@manager.option('-p', '-passwd', dest='passwd')
@manager.option('-e', '-email', dest='email')
def createsuperuser(dmp_username, real_name, passwd, email):
    """创建管理员用户"""
    from dmp.models import Users, Groups
    from dmp.utils.ep_data import EnvelopedData
    if not all([dmp_username, real_name, passwd, email]):
        return 'Insufficient parameter, please recreate superuser.'

    db_user_count = Users.query.count()
    if db_user_count == 0:
        user = Users(dmp_username=dmp_username, real_name=real_name, password=passwd, email=email)
        rootgroup = Groups.query.filter(Groups.id == 1).first()
        user.dmp_group_id = 1
        user.leader_dmp_user_id = None
        db.session.add(user)
        db.session.commit()
        res = EnvelopedData.create_root(rootgroup, user, email)
        if isinstance(res, str):
            return {'msg': res}
        return {'msg': 'The email of the register root has been sent, please click activate.'}
    else:
        return {'msg': 'The super administrator already exists in the database, please do not add it again.'}


if __name__ == '__main__':
    manager.run()
