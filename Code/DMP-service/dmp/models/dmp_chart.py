#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/19
# @Author  : SHTD

import datetime
from dmp.extensions import db
from dmp.models import DMPModel


class Chart(db.Model, DMPModel):
    """图表表"""
    __tablename__ = 'dmp_chart'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, comment='看板ID')
    chart_name = db.Column(db.String(64), nullable=False, comment='图标名称')
    dmp_data_table_id = db.Column(db.Integer, nullable=False, comment='数据表ID')
    query_string = db.Column(db.Text, nullable=False, comment='查询语句')
    chart_data = db.Column(db.Text, nullable=False, comment='数据')
    chart_type = db.Column(db.Integer, nullable=False,
                           comment='图表类型，柱状图1，折线图2，饼图3，地图4，雷达图5')
    params = db.Column(db.Text, nullable=False, comment='图表参数')
    update_interval = db.Column(
        db.Integer, default=0, nullable=False, comment='时间间隔时间')
    update_unit = db.Column(db.Integer, default=0,
                            nullable=False, comment='时间间隔单位，0小时，1日，3周')
    description = db.Column(db.String(512), comment='简介')
    dmp_dashboard_id = db.Column(db.Integer, nullable=False, comment='数据看板ID')

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

    @property
    def _json_tmp(self):
        _d = {
            "created_dmp_user_name": self.created_dmp_user_name,
            "changed_dmp_user_name": self.changed_dmp_user_name,
            "dmp_data_table_name": dmp_data_table_name,
        }
        return _d
