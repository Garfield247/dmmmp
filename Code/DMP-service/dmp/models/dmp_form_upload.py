#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

import datetime
from dmp.extensions import db
from dmp.models import DMPModel


class FormUpload(db.Model, DMPModel):
    """数据文件上传表单表"""
    __tablename__ = 'dmp_form_upload'
    fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filetype = db.Column(db.Integer, nullable=False, comment='文件类型')
    filepath = db.Column(db.String(256), nullable=False, comment='文件路径')
    column_line = db.Column(db.Integer, comment='列名行号')
    column = db.Column(db.String(32), comment='自定义列名')
    method = db.Column(db.Integer, default=1, comment='新建1、添加2或覆盖3')
    destination_dmp_database_id = db.Column(db.Integer,  nullable=False,comment='目标数据库ID')
    destination_db_table_name  = db.Column(db.String(32), nullable=False, comment='数据库内数据表名称')
    dmp_case_id = db.Column(db.Integer, nullable=False, comment='所属案例')
    dmp_data_table_name = db.Column(db.String(32), unique=True, nullable=False, comment='数据名称')


    @property
    def destination_database_name(self):
        from dmp.models import Database
        d = Database.get(self.destination_dmp_database_id)
        d_name = d.dmp_database_name if d else "-"
        return d_name

    @property
    def dmp_case_name(self):
        from dmp.models import Case
        c = Case.get(self.dmp_case_id)
        c_name = c.dmp_case_name if c else "-"
        return c_name

    @property
    def _json_tmp(self):
        _d = {
            "dmp_case_name":self.dmp_case_name,
            "destination_database_name":self.destination_database_name,
        }
        return _d