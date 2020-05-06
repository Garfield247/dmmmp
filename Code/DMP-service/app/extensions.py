#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

#导入类库
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate


#创建对象
db = SQLAlchemy()
mail = Mail()
migrate = Migrate(db = db)


#初始化
def config_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app)
