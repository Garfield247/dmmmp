#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

import os
from flask_script import Manager,Server
from dmp import app
from flask_migrate import MigrateCommand




#创建命令起动控制对象
manager = Manager(app)
# 添加数据库迁移命令
manager.add_command('db', MigrateCommand)
# 添加服务配置
manager.add_command('runserver',Server(host='0.0.0.0',port=7789))

#路由列表命令
@manager.command
def url_map():
    app.logger.info(app.url_map)

if __name__ == '__main__':
    manager.run()

