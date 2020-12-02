#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

import os
import logging
from flask import Flask
from dmp.config import config
from dmp.extensions import config_extensions
from dmp.api import config_blueprint
from dmp.utils.rbac import rbac_middleware

# 封装一个方法，专门用于创建Flask实例


def create_app(config_name):
    # 创建应用实例
    app = Flask(__name__)
    # 初始化配置
    app.config.from_object(config.get(config_name) or config['default'])
    # 调用初始化函数
    config[config_name].init_app(app)
    # 配置日志等级
    app.logger.setLevel(logging.ERROR)
    # 配置扩展
    config_extensions(app)
    # 配置蓝本
    config_blueprint(app)

    # RBAC权限拦截
    app.before_request(rbac_middleware)

    # 返回应用实例
    return app


# 获取配置
config_name = os.environ.get('DMP_CONFIG') or 'testing'

# 创建实例
app = create_app(config_name)



def get_app():
    return app
