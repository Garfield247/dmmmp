#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from dmp.extensions import db
from dmp.models import DMPModel


class DataTableColumnRange(db.Model, DMPModel):
    """数据列区间表"""
    __tablename__ = 'dmp_data_table_column_range'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    context = db.Column(db.String(256), comment='内容')
    dmp_data_table_column_id = db.Column(db.Integer, db.ForeignKey('dmp_data_table_column.id'), nullable=False,
                                         comment='列ID')

    # data_table_column = db.relationship('DataTableColumn', backref='table_column_range')
