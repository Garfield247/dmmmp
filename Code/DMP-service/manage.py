#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from flask_script import Manager,Server
from flask_migrate import MigrateCommand
from dmp import app
from dmp.extensions import db


# 创建命令起动控制对象
manager = Manager(app)
# 添加数据库迁移命令
manager.add_command('db', MigrateCommand)
# 添加服务配置
manager.add_command('runserver',Server(host='0.0.0.0',port=7789,use_debugger=True))

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
    from dmp.models import Users,Case,Database
    from dmp.api.dbtable import post
    count = 30
    for i in range(count):
        new_test_table = post(
            dmp_data_table_name="dmp_test_dbtable_%d"%i,
            db_table_name="dmp_test_db_table_name%d"%i,
            description="测试表",
            dmp_user_id=random.choice(Users.query.all()).id,
            dmp_database_id=random.choice(Database.query.all()).id,
            dmp_case_id=random.choice(Case.query.all()).id
        )
        app.logger.info("add test data :"+str(new_test_table))

# 初始化
@manager.command
def sys_init():
    db.drop_all()
    db.create_all()
    from dmp.models import Permissions
    Permissions.init_permission()
    from dmp.models import Group
    Group.init_group()
    from dmp.models import Users
    Users.create_test_user()

if __name__ == '__main__':
    manager.run()

