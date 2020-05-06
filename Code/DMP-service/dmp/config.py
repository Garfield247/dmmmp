#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

#通用配置
import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SHTD123.'

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or ''
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or ''
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')or ''

    CELERY_RESULT_BACKEND = "redis://localhost:6379/1/"
    CELERY_BROKER_URL = "redis://localhost:6379/2"

    @staticmethod
    def init_app(app):
        pass
#开发环境
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir,'dmp-dev.sqlite')

#测试环境
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir,'dmp-test.sqlite')

#生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir,'dmp.sqlite')

#配置字典
config = {
    'development':DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default':DevelopmentConfig,
}

