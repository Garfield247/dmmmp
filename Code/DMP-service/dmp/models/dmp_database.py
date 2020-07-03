#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

import datetime
from dmp.extensions import db
from dmp.models import DMPModel


class Database(db.Model, DMPModel):
    """数据库表"""
    __tablename__ = 'dmp_database'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_database_name = db.Column(db.String(32), unique=True, nullable=False, comment='数据显示名称')
    db_type = db.Column(db.Integer, nullable=False, comment='数据库类型,hive:0,mysql:1,mongo:2')
    db_host = db.Column(db.String(32), nullable=False, comment='数据库主机地址')
    db_port = db.Column(db.Integer, nullable=False, comment='数据库端口号')
    db_name = db.Column(db.String(32), comment='数据库名称')
    db_username = db.Column(db.String(32), comment='数据库用户名')
    db_passwd = db.Column(db.String(64), comment='数据库密码')
    ispublic = db.Column(db.Boolean, default=False,comment='是否公开')
    description = db.Column(db.String(128), comment='数据库说明')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), nullable=False, comment='所属用户ID')

    users = db.relationship('Users', backref='database')
