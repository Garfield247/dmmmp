#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

import datetime
from dmp.extensions import db

class FromAddDataTable(db.Model):
    """数据从数据库添加表单表"""
    __tablename__ = 'dmp_from_add_data_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_data_table_name = db.Column(db.String(64), unique=True, comment='数据名称')
    db_table_name = db.Column(db.String(32), nullable=False, comment='数据库内数据表名称')
    submit_on = db.Column(db.DateTime, nullable=False, comment='提交时间')
    description = db.Column(db.String(128), comment='说明')
    approve_on = db.Column(db.DateTime, comment='审批时间')
    approve_result = db.Column(db.Integer, comment='审批结果,默认:0,通过:1,不通过:2')
    answer = db.Column(db.String(32), comment='审批答复')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    submit_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), nullable=False, comment='提交人')
    dmp_database_id = db.Column(db.Integer, db.ForeignKey('dmp_database.id'), nullable=False, comment='数据库ID')
    dmp_case_id = db.Column(db.Integer, db.ForeignKey('dmp_data_case.id'), nullable=False, comment='所属案例ID')
    approve_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), comment='审批人')

    submit_users = db.relationship('Users', backref='submitusers_from_add_data_table')
    approve_users = db.relationship('Users', backref='approveusers_from_add_data_table')
    database = db.relationship('Database', backref='database_from_add_data_table')
    datacase = db.relationship('DataCase', backref='datacase_from_add_data_table')
