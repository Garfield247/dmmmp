#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from dmp.extensions import db
from dmp.models import DMPModel


class DataTableColumn(db.Model, DMPModel):
    """数据列信息表"""
    __tablename__ = 'dmp_data_table_column'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_data_table_column_name = db.Column(db.String(32), nullable=False, comment='列名')
    groupby = db.Column(db.Boolean, default=False, comment='可以进行分组')
    wherein = db.Column(db.Boolean, default=False, comment='可以区间筛选')
    isdate = db.Column(db.Boolean, default=False, comment='是否为时间日期字段')
    description = db.Column(db.String(128), comment='字段说明')
    dmp_data_table_id = db.Column(db.Integer, db.ForeignKey('dmp_data_table.id'), nullable=False, comment='数据ID')

    # datatable = db.relationship('DataTable', backref='data_table_column')
