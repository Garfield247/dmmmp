#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD


from .main import main
from .case import case
from .database import database
from .dbtable import dbtable
from .file import file
from .form import form
from .permission import permission
from .rights import rights
from .user import user
from .usergroup import usergroup
from .verifier import verifier

# 蓝本配置
DEFAULT_BLUEPRINT = (
    (main, '/'),
    (case, '/case'),
    (database, '/database'),
    (dbtable, '/dbtable'),
    (file, '/file'),
    (form, '/form'),
    (permission, '/permission'),
    (rights, '/rights'),
    (user, '/user'),
    (usergroup, '/usergroup'),
    (verifier, '/verifier'),
)


# 封装函数，完成蓝本注册
def config_blueprint(app):
    for blueprint, prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=prefix)
