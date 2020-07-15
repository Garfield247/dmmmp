#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

import datetime
from dmp.extensions import db
from dmp.models import DMPModel


class FormAddDataTable(db.Model, DMPModel):
    """数据从数据库添加表单表"""
    __tablename__ = 'dmp_form_add_data_table'
    fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_data_table_name = db.Column(db.String(64), comment='数据名称')
    db_table_name = db.Column(db.String(32), nullable=False, comment='数据库内数据表名称')
    dmp_database_id = db.Column(db.Integer,  nullable=False, comment='数据库ID')
    dmp_case_id = db.Column(db.Integer,  nullable=False, comment='所属案例ID')

    @property
    def dmp_database_name(self):
        from dmp.models import Database
        d = Database.get(self.dmp_database_id)
        d_name = d.dmp_database_name if d else "-"
        return d_name

    @property
    def dmp_case_name(self):
        from dmp.models import Case
        c = Case.get(self.dmp_case_id)
        c_name = c.dmp_case_name if c else "-"
        return c_name


    @property
    def _json_cache(self):
        _d = {
            "submit_dmp_username":self.submit_dmp_username,
            "approve_dmp_username": self.approve_dmp_username,
            "dmp_case_name":self.dmp_case_name,
            "dmp_database_name":self.dmp_database_name,
        }
        return _d