#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD
import datetime

from dmp.extensions import db
from dmp.models import DMPModel


class UserDataService(db.Model, DMPModel):
    """用户服务访问关联表"""
    __tablename__ = 'dmp_user_data_service'
    dmp_user_id = db.Column(db.Integer, nullable=False, comment='用户ID')
    dmp_data_service_id = db.Column(db.Integer, nullable=False, comment='数据服务ID')
    access_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='到访时间')