#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

import datetime
from dmp.extensions import db
from dmp.models import DMPModel


class FromUpload(db.Model, DMPModel):
    """数据文件上传表单表"""
    __tablename__ = 'dmp_from_upload'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filetype = db.Column(db.Integer, nullable=False, comment='文件类型')
    filepath = db.Column(db.String(256), nullable=False, comment='文件路径')
    column_line = db.Column(db.Integer, comment='列名行号')
    column = db.Column(db.String(32), comment='自定义列名')
    json_dimension_reduction = db.Column(db.Boolean, comment='json数据是否遍历存储')
    method = db.Column(db.Integer, default=1, comment='新建1、添加2或覆盖3')
    description = db.Column(db.String(128), comment='说明')
    submit_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False, comment='提交时间')
    approve_on = db.Column(db.DateTime, onupdate=datetime.datetime.now, comment='审批时间')
    approve_result = db.Column(db.Integer, default=0, comment='审批结果,默认:0,通过:1,不通过:2')
    answer = db.Column(db.String(32), comment='审批答复')
    upload = db.Column(db.Boolean, comment='是否成功')
    upload_result = db.Column(db.Text, comment='数据上传结果')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    submit_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), nullable=False, comment='提交人')
    destination_dmp_database_id = db.Column(db.Integer, db.ForeignKey('dmp_database.id'), nullable=False,comment='目标数据库ID')
    destination_db_table_name  = db.Column(db.String(32), nullable=False, comment='数据库内数据表名称')
    dmp_case_id = db.Column(db.Integer, db.ForeignKey('dmp_case.id'), nullable=False, comment='所属案例')
    dmp_data_table_name = db.Column(db.String(32), unique=True, nullable=False, comment='数据名称')
    approve_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), comment='审批人')

    form_type = db.Column(db.Integer, default=2, comment='表单类型')

    submit_users = db.relationship('Users', foreign_keys=submit_dmp_user_id, backref='submitusers_from_upload')
    approve_users = db.relationship('Users', foreign_keys=approve_dmp_user_id, backref='approveusers_from_upload')
    database = db.relationship('Database',foreign_keys=destination_dmp_database_id, backref='database_from_upload')
    datacase = db.relationship('Case', foreign_keys=dmp_case_id,backref='case_from_upload')
