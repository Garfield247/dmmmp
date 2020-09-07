#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/19
# @Author  : SHTD

import datetime
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
        db.Integer, comment='数据表ID')
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

    def delete(self):
        from dmp.models import DataServiceParameter
        count = DataServiceParameter.query.filter_by(dmp_data_service_id=self.id).count()
        if count > 0:
            parameters = DataServiceParameter.query.filter_by(dmp_data_service_id=self.id)
            parameters.delete()
            db.session.delete(self)
        else:
            db.session.delete(self)


    @classmethod
    def exsit_data_service_by_name(cls, ds_name):
        item = cls.query.filter_by(data_service_name=ds_name).first()
        if item:
            return True
        return False

    @classmethod
    def exsit_data_service_by_apipath(cls, apipath):
        item = cls.query.filter_by(api_path=apipath).first()
        if item:
            return True
        return False

    def delete(self):
        try:
            from .dmp_data_service_parameter import DataServiceParameter
            DataServiceParameter.query.filter_by(
                dmp_data_service_id=self.id).delete()
            db.session.delete(self)
        except Exception as err:
            raise err

    @property
    def params(self):

        from .dmp_data_service_parameter import DataServiceParameter
        _params = DataServiceParameter.query.filter_by(
            dmp_data_service_id=self.id).all()
        res = [{"parameter_name": p.parameter_name, "required": bool(
            p.required_parameter)} for p in _params]
        return res

    @ property
    def source_dmp_data_table_name(self):
        from .dmp_data_table import DataTable
        if DataTable.exist_item_by_id(self.source_dmp_data_table_id):
            data_table_name = DataTable.get(
                self.source_dmp_data_table_id).db_table_name
            return data_table_name
        return "-"

    @ property
    def _json_tmp(self):
        _d = {
            "created_dmp_user_name": self.created_dmp_user_name,
            "changed_dmp_user_name": self.changed_dmp_user_name,
            "source_dmp_data_table_name": self.source_dmp_data_table_name,
        }
        return _d
