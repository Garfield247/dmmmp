#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

import datetime
from dmp.extensions import db
from dmp.models import DMPModel


class FromDownload(db.Model, DMPModel):
    """数据下载表单表"""
    __tablename__ = 'dmp_from_download'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rule = db.Column(db.String(64), comment='数据库提取规则')
    description = db.Column(db.Text, comment='说明')
    submit_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False, comment='提交时间')
    approve_on = db.Column(db.DateTime, comment='审批时间')
    approve_result = db.Column(
        db.Integer, default=0, comment='审批结果,默认:0,通过:1,不通过:2')
    answer = db.Column(db.String(32), comment='审批答复')
    ftp_url = db.Column(db.String(64), comment='FTP下载链接')
    ftp_pid = db.Column(db.Integer, comment='FTP进程号')
    filepath = db.Column(db.String(128), comment='文件路径')
    finish = db.Column(db.Boolean, comment='是否完成')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    submit_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), nullable=False, comment='提交人')
    dmp_data_table_id = db.Column(db.Integer, db.ForeignKey('dmp_data_table.id'), nullable=False, comment='源数据表ID')
    approve_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), comment='审批人')

    form_type = db.Column(db.Integer, default=4, comment='表单类型')

    submit_users = db.relationship('Users', foreign_keys=submit_dmp_user_id, backref='submitusers_from_download')
    approve_users = db.relationship('Users', foreign_keys=approve_dmp_user_id, backref='approveusers_from_migrate')
    datatable = db.relationship('DataTable', backref='datatable_from_download')
