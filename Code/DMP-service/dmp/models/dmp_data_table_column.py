#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import current_app
from dmp.extensions import db
from dmp.models import DMPModel


class DataTableColumn(db.Model, DMPModel):
    """数据列信息表"""
    __tablename__ = 'dmp_data_table_column'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_data_table_column_name = db.Column(db.String(32), nullable=False, comment='列名')
    dmp_data_table_column_type = db.Column(db.String(32), comment='数据类型')
    groupby = db.Column(db.Boolean, default=False, comment='可以进行分组')
    wherein = db.Column(db.Boolean, default=False, comment='可以区间筛选')
    isdate = db.Column(db.Boolean, default=False, comment='是否为时间日期字段')
    description = db.Column(db.String(128), comment='字段说明')
    dmp_data_table_id = db.Column(db.Integer, db.ForeignKey('dmp_data_table.id'), nullable=False, comment='数据ID')

    # datatable = db.relationship('DataTable', backref='data_table_column')
    def delete(self):
        from dmp.models import DataTableColumnRange
        data_table_columns_range = DataTableColumnRange.query.filter_by(
            dmp_data_table_column_id=self.id).all()
        for dtc in data_table_columns_range:
            current_app.logger.info(dtc.__json__())
            dtc.delete()
        db.session.delete(self)
