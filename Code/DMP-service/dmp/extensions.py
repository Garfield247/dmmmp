#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

# 导入类库
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_cors import CORS
from flask_celery import Celery
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 创建对象
db = SQLAlchemy()
mail = Mail()
migrate = Migrate(db=db)
cors = CORS()
celery = Celery()
limiter = Limiter(key_func=get_remote_address, headers_enabled=True)


# 初始化
def config_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app)
    cors.init_app(app, supports_credentials=True)
    celery.init_app(app)
    limiter.init_app(app)
