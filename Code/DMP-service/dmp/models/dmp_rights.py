#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from dmp.extensions import db
from dmp.models import DMPModel

class Rights(db.Model,DMPModel):
    """权利表"""
    __tablename__ = 'dmp_rights'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='功能ID')
    dmp_rights_name = db.Column(db.String(32), nullable=False, comment='路由功能名称')