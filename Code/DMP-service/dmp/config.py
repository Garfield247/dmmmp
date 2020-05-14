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

    LEADER_ROOT_ID = 1

    @staticmethod
    def init_app(app):
        pass
#开发环境
class DevelopmentConfig(Config):
    TESTING = True
    LOG_LEVE = "info"
    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.163.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '15010080053@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')or 'KPIKDLKPCQSQELTF'
    # Celery
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1/"
    CELERY_BROKER_URL = "redis://localhost:6379/2"
    # DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir,'dmp-dev.sqlite')
<<<<<<< HEAD
    # UPLOADED
    UPLOADED_PATH = os.path.join(base_dir,"static/upload")
=======
    DEBUG = True
    # White_list
    WHITE_LIST = [
        r"^/user/login/",
        r"^/static/",
        r"^/user/register/$",
        r"^/user/logout/$",
        r"^/user/icon/$",
        r"^/user/activate/.*",
        r"^/verifier/email/",
        r"^/verifier/username/",
    ]
    # 免认证
    NO_PERMISSION_LIST = [
        r'^/user/index/$',
    ]
>>>>>>> 86cec918be112616cf9c9d2bd61ae808ed8b2538

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
    # UPLOADED
    UPLOADED_PATH = os.path.join(base_dir,"static/upload")

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
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

