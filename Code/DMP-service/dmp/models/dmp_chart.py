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
    chart_name = db.Column(db.String(64), nullable=False, comment='图表名称')
    dmp_data_table_id = db.Column(db.Integer,  comment='数据表ID')
    query_string = db.Column(db.JSON, comment='查询语句')
    chart_data = db.Column(db.JSON, comment='数据')
    chart_type = db.Column(db.Integer, nullable=False,
                           comment='图表类型，柱状图1，折线图2，饼图3，地图4，雷达图5')
    params = db.Column(db.Text,  comment='图表参数')
    update_interval = db.Column(
        db.Integer, default=0, comment='时间间隔时间')
    update_unit = db.Column(db.Integer, default=0,
                             comment='时间间隔单位，0小时，1日，3周')
    description = db.Column(db.String(512), comment='简介')
    charts_position = db.Column(db.JSON, nullable=False, comment='图表布局数据')
    dmp_dashboard_id = db.Column(db.Integer, nullable=False, comment='数据看板ID')
    update_task_id = db.Column(db.String(64), comment='更新任务ID')
    created_dmp_user_id = db.Column(db.Integer, nullable=False, comment='创建人')
    changed_dmp_user_id = db.Column(db.Integer, comment='修改人')
    created_on = db.Column(
        db.DateTime, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, comment='最后修改时间')

    def chart_to_dict(self):
        chart_dict = {
            'id': self.id,
            'chart_name': self.chart_name,
            'dmp_data_table_id': self.dmp_data_table_id,
            'query_string': self.query_string,
            'chart_data': self.chart_data,
            'chart_type': self.chart_type,
            'params': self.params,
            'update_interval': self.update_interval,
            'update_unit': self.update_unit,
            'description': self.description,
            'charts_position': self.charts_position,
            'dmp_dashboard_id': self.dmp_dashboard_id,
            'update_task_id': self.update_task_id,
            'created_dmp_user_id': self.created_dmp_user_id,
            'changed_dmp_user_id': self.changed_dmp_user_id,
            'created_on': self.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            'changed_on': self.changed_on.strftime("%Y-%m-%d %H:%M:%S")
        }
        return chart_dict
        
    def delete(self):
        from dmp.extensions import apscheduler
        apscheduler.delete_job(id=self.update_task_id)
        db.session.delete(self)
        db.session.commit()


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
