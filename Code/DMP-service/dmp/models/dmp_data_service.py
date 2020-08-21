#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/19
# @Author  : SHTD

from dmp.extensions import db
from dmp.models import DMPModel


class DataService(db.Model, DMPModel):
    """数据服务表"""
    __tablename__ = 'dmp_data_service'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, comment='看板ID')
    data_service_name = db.Column(
        db.String(64), nullable=False, comment='数据服务名称')
    request_method = db.Column(
        db.Integer, default=1, comment='请求方法，1GET 2POST')
    api_path = db.Column(db.String(256), unique=True,
                         nullable=False, comment='API地址')
    source_dmp_data_table_id = db.Column(
        db.Integer, nullable=False, comment='数据表ID')
    query_sql = db.Column(db.Text, comment='查询语句，MySQL必须项')
    query_params = db.Column(db.Text, comment='查询参数，MongoDB必须项')
    state = db.Column(db.Integer, default=0, comment='是否启用')
    description = db.Column(db.String(512), comment='服务简介')

    created_dmp_user_id = db.Column(db.Integer, nullable=False, comment='创建人')
    changed_dmp_user_id = db.Column(db.Integer, comment='修改人')
    created_on = db.Column(
        db.DateTime, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, comment='最后修改时间')

    @classmethod
    def exsit_data_service_by_name(cls, ds_name):
        item = cls.query.filter_by(data_service_name=ds_name).first()
        if item:
            return True
        return False

    @classmethod
    def exsit_data_service_by_apipath(cls, apipath):
        item = cls.query.filter_by(cls.api_path=apipath).first()
        if item:
            return True
        return False

    @property
    def source_dmp_data_table_name(self):
        from .dmp_data_table import DataTable
        if DataTable.exist_item_by_id(self.source_dmp_data_table_id):
            data_table_name = DataTable.get(
                self.source_dmp_data_table_id).data_table_name
            return data_table_name
        return "-"
