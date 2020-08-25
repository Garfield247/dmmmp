#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

import datetime
from dmp.extensions import db
from dmp.models import DMPModel


class UserDashboard(db.Model, DMPModel):
    """主页看板用户关联表"""
    __tablename__ = 'dmp_user_dashboard'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, comment='ID')
    dmp_user_id = db.Column(db.Integer, nullable=False, comment='用户ID')
    dmp_dashboard_id = db.Column(db.Integer, nullable=False, comment='看板ID')
