#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from flask import Flask
from dmp.config import config
from dmp.extensions import config_extensions
from dmp.api import config_blueprint
#封装一个方法，专门用于创建Flask实例
def create_app(config_name):
    #创建应用实例
    app = Flask(__name__)
    #初始化配置
    app.config.from_object(config.get(config_name) or config['default'])
    #调用初始化函数
    config[config_name].init_app(app)
    #配置扩展
    config_extensions(app)
    #配置蓝本
    config_blueprint(app)
    #返回应用实例
    return app
