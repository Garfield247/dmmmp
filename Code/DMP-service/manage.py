#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

import os
from flask_script import Manager,Server
from flask_migrate import MigrateCommand
from flask import current_app
from dmp import app
from dmp.extensions import db



# 创建命令起动控制对象
manager = Manager(app)
# 添加数据库迁移命令
manager.add_command('db', MigrateCommand)
# 添加服务配置
manager.add_command('runserver',Server(host='0.0.0.0',port=7789))

# 路由列表命令
@manager.command
def url_map():
    for i in app.url_map.__dict__.get("_rules"):
        app.logger.info([i.rule,i.defaults])



# 删除所有表
@manager.command
def drop_db():
    app.logger.info("drop db")
    db.drop_all()

# 创建所有表
@manager.command
def create_db():
    db.create_all()

# 初始化
@manager.command
def sys_init():
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    manager.run()

