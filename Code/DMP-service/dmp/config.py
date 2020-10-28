#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

# 通用配置
import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SHTD123.'
    # DB
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # White_list
    WHITE_LIST = [
        r"^/user/login/",
        r"^/static/.*",
        r"^/user/register/$",
        r"^/user/icon/$",
        r"^/user/activate/.*",
        r"^/user/changepwd/",
        r"^/user/forgetpwd/",
        r"^/verifier/.*",
        r"^/file/upload/",
        r"^/file/success/",
        r"^/database/connect/",
        r"^/index/.*"
        r"^/ds/api/.*"
    ]
    # 免认证
    NO_PERMISSION_LIST = [
        r'^/user/index/$',
    ]

    @staticmethod
    def init_app(app):
        pass


# 开发环境
class DevelopmentConfig(Config):
    # TESTING = True
    LOG_LEVE = "error"
    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.163.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '15010080053@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'KPIKDLKPCQSQELTF'
    # Celery
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1/"
    CELERY_BROKER_URL = "redis://localhost:6379/2"
    # DB

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    # os.path.join(base_dir, 'dmp-dev.sqlite')

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:shtd123.@192.168.3.87:3306/dmpdb?charset=utf8"
    # UPLOADED
    UPLOADED_PATH = os.path.join(base_dir, "static/upload")

    # DataX
    DATAX_PATH = os.environ.get("DATAX_HOME") or ""
    DATAX_JOB_PATH = os.environ.get("DATAX_JOB_PATH") or ""
    DATAX_LOG_PATH = os.environ.get("DATAX_LOG_PATH") or ""

    DEBUG = True

    # ICON_URL
    SAVE_URL = 'dmp/static/icon/'
    ICON_URL = 'http://192.168.3.87:7789/static/icon/'

    JOBS = []
    SCHEDULER_API_ENABLED = True
    SCHEDULER_JOBSTORES = {"default": SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)}
    SCHEDULER_TIMEZONE = "UTC"
    # SCHEDULER_EXECUTORS = {
	# 'default': {'type': 'threadpool', 'max_workers': 20}
    # }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 5
    }

    # KYLIN
    KYLIN_HOST = "192.168.3.60"
    KYLIN_PORT = "7070"
    KYLIN_NAME = "ADMIN"
    KYLIN_PASSWD = "KYLIN"
    KYLIN_PROJECT = "dmp_test"



# 测试环境
class TestingConfig(Config):
    # Mail
    # TESTING = True
    LOG_LEVE = "error"
    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.shtdtech.com'
    EMAIL_PORT = 25
    EMAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get(
        'MAIL_USERNAME') or 'dmp.service@shtdtech.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'shtd.123'
    # Celery
    CELERY_RESULT_BACKEND = "redis://192.168.3.87:6379/1"
    CELERY_BROKER_URL = "amqp://dmp:dmp123.@192.168.3.87:5672/dmpvhost"
    # db
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:shtd123.@192.168.3.87:3306/dmpdb?charset=utf8mb4"
    # UPLOADED
    UPLOADED_PATH = os.environ.get("DMP_UPLOAD_PATH") or "/home/dmp/dmp_upload"
    # UPLOADED_PATH = os.path.join(base_dir, "static/upload")
    DOWNLOAD_PATH = os.environ.get(
        "DMP_DOWNLOAD_PATH") or "/home/dmp/dmp_download"

    # DataX
    DATAX_HOME = os.environ.get("DATAX_HOME") or "/home/dmp/datax"
    DATAX_JOB_PATH = os.environ.get("DATAX_JOB_PATH") or "/home/dmp/dmp_job"
    DATAX_LOG_PATH = os.environ.get(
        "DATAX_LOG_PATH") or "/home/dmp/dmp_log/datax"

    # ICON_URL
    SAVE_URL = os.path.join(base_dir, "static/icon")
    ICON_URL = 'http://192.168.3.87:7789/static/icon/'

    JOBS = []
    SCHEDULER_API_ENABLED = True
    SCHEDULER_JOBSTORES = {"default": SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)}
    SCHEDULER_TIMEZONE = "UTC"
    # SCHEDULER_EXECUTORS = {
	# 'default': {'type': 'threadpool', 'max_workers': 20}
    # }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 5
    }
    # KYLIN
    KYLIN_HOST = "192.168.3.60"
    KYLIN_PORT = "7070"
    KYLIN_NAME = "ADMIN"
    KYLIN_PASSWD = "KYLIN"
    KYLIN_PROJECT = "dmp_test"

# 生产环境
class ProductionConfig(Config):
    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or ''
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or ''
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''
    # Celery
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1/"
    CELERY_BROKER_URL = "redis://localhost:6379/2"
    # DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(base_dir, 'dmp.sqlite')


# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
