#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/19
# @Author  : SHTD

from dmp.extensions import db
from dmp.models import DMPModel


class SavedQuery(db.Model, DMPModel):
    """已保存查询表"""
    __tablename__ = 'dmp_saved_query'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, comment='看板ID')
    query_name = db.Column(db.String(64), nullable=False, comment='查询语句的保存名称')
    query_sql = db.Column(db.Text, nullable=False, comment='查询语句')
    description = db.Column(db.String(512), comment='备注')
    dmp_data_table_id = db.Column(db.Integer, nullable=False, comment='数据表ID')
    dmp_case_id = db.Column(db.Integer, nullable=False, comment='所属案例ID')

    created_dmp_user_id = db.Column(db.Integer, nullable=False, comment='创建人')
    changed_dmp_user_id = db.Column(db.Integer, comment='修改人')
    created_on = db.Column(
        db.DateTime, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, comment='最后修改时间')

    @property
    def dmp_data_table_name(self):
        from .dmp_data_table import DataTable
        if DataTable.exist_item_by_id(self.dmp_data_table_id):
            data_table_name = DataTable.get(
                self.dmp_data_table_id).dmp_data_table_name
            return data_table_name
        return "-"
