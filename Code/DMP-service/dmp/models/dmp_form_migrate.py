#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

import datetime
from dmp.extensions import db
from dmp.models import DMPModel


class FormMigrate(db.Model, DMPModel):
    """数据迁移表单表"""
    __tablename__ = 'dmp_form_migrate'
    fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    origin_dmp_table_id = db.Column(db.Integer, nullable=False, comment='起点数据表')
    new_table_name = db.Column(db.String(32), nullable=False, comment='新表名')
    destination_dmp_database_id = db.Column(db.Integer, nullable=False,comment='目标数据库ID')

    @property
    def destination_dmp_database_name(self):
        from dmp.models import Database
        d = Database.get(self.destination_dmp_database_id)
        d_name = d.dmp_database_name if d else "-"
        return d_name

    @property
    def origin_data_table_name(self):
        from dmp.models import DataTable
        t = DataTable.get(self.origin_dmp_table_id)
        t_name = t.dmp_data_table_name if t else "-"
        return t_name

    @property
    def _json_tmp(self):
        _d = {
            "origin_data_table_name":self.origin_data_table_name,
            "destination_dmp_database_name":self.destination_dmp_database_name,
        }
        return _d