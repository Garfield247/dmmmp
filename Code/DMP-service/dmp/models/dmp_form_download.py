#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

import datetime
from dmp.extensions import db
from dmp.models import DMPModel


class FormDownload(db.Model, DMPModel):
    """数据下载表单表"""
    __tablename__ = 'dmp_form_download'
    fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_data_table_id = db.Column(db.Integer, nullable=False, comment='源数据表ID')
    ftp_url = db.Column(db.String(128), comment='FTP下载链接')
    filepath = db.Column(db.String(128), comment='文件路径')





    @property
    def data_table_name(self):
        from dmp.models import DataTable
        t = DataTable.get(self.dmp_data_table_id)
        t_name = t.dmp_data_table_name if t else "-"
        return t_name

    @property
    def dmp_case_name(self):
        from dmp.models import Case
        c = Case.get(self.dmp_case_id)
        c_name = c.dmp_case_name if c else "-"
        return c_name

    @property
    def _json_cache(self):
        _d = {
            "dmp_case_name":self.dmp_case_name,
            "data_table_name":self.data_table_name,
        }
        return _d