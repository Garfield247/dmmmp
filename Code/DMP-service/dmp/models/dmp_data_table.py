#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

import datetime
from dmp.extensions import db
from .dmp_user import Users
from dmp.models import DMPModel

class DataTable(db.Model,DMPModel):
    """数据表"""
    __tablename__ = 'dmp_data_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_data_table_name = db.Column(db.String(32), unique=True, nullable=False, comment='数据名称')
    db_table_name = db.Column(db.String(32), nullable=False, comment='数据库内数据表名称')
    description = db.Column(db.String(128), comment='数据说明')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), nullable=False, comment='添加人')
    dmp_database_id = db.Column(db.Integer, db.ForeignKey('dmp_database.id'), nullable=False, comment='数据库ID')
    dmp_case_id = db.Column(db.Integer, db.ForeignKey('dmp_case.id'), nullable=False, comment='所属案例ID')

    # users = db.relationship('Users', backref='users_datatable')
    # database = db.relationship('Database', backref='database_datatable')
    # case = db.relationship('Case', backref='case_datatable')