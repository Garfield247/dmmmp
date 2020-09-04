#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

import datetime

from dmp.extensions import db
from dmp.models import DMPModel


class DataServiceParameter(db.Model, DMPModel):
    """数据服务表"""
    __tablename__ = 'dmp_data_service_parameter'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, comment='参数ID')
    dmp_data_service_id = db.Column(
        db.Integer, nullable=False, comment='数据服务ID')
    parameter_name = db.Column(
        db.String(128), nullable=False, comment='参数名(要进行筛选的字段名)')
    type = db.Column(db.String(64), default='-', comment='参数类型。取决于源数据表的类型定义')
    required_parameter = db.Column(db.Integer, default=0, comment='是否为必填项')
    description = db.Column(db.String(512), comment='简介')


    def save_bulk(self, objects):
        item = objects[0]
        dmp_data_service_id = item.dmp_data_service_id
        parameters = DataServiceParameter.query.filter_by(dmp_data_service_id=dmp_data_service_id)
        count = parameters.count()
        if count > 0:
            parameters.delete()
        db.session.add_all(objects)
        db.session().commit()