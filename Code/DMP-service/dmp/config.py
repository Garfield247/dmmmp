#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

#通用配置
import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SHTD123.'
    # DB
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass
#开发环境
class DevelopmentConfig(Config):
    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or ''
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or ''
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')or ''
    # Celery
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1/"
    CELERY_BROKER_URL = "redis://localhost:6379/2"
    # DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir,'dmp-dev.sqlite')

#测试环境
class TestingConfig(Config):
    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or ''
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or ''
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')or ''
    # Celery
    CELERY_RESULT_BACKEND = "redis://192.168.3.87:6379/1"
    CELERY_BROKER_URL = "amqp://dmp:dmp123.@192.168.3.87:5672/dmpvhost"
    # db
    SQLALCHEMY_DATABASE_URI = "mysql://root:shtd123.@192.168.3.87/3306/dmpdb?charset=utf-8"


#生产环境
class ProductionConfig(Config):
    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or ''
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or ''
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')or ''
    # Celery
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1/"
    CELERY_BROKER_URL = "redis://localhost:6379/2"
    # DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir,'dmp.sqlite')

#配置字典
config = {
    'development':DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default':DevelopmentConfig,
}

