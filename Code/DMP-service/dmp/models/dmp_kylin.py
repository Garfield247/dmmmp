#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/10/20
# @Author  : SHTD
import datetime
from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property

from dmp.extensions import db
from dmp.models import DMPModel


class KylinTable(db.Model, DMPModel):
    """kylin表"""
    __tablename__ = 'dmp_kylin_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kylin_cube_name = db.Column(
        db.String(64), unique=True, nullable=False, comment='cube名称')
    kylin_models_name = db.Column(
        db.String(64), unique=True, nullable=False, comment='model名称')
    db_table_name = db.Column(
        db.String(64), nullable=False, comment='数据库内数据表名称')
    is_kylin = db.Column(db.Integer, default=0, comment='是否是Kylin表,0否，1是， 2转化中 ')
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, comment='修改时间')



    @classmethod
    def exist_item_by_db_table_name(cls, table_name):
        item = cls.query.filter_by(db_table_name=table_name).first()
        if item:
            return True
        return False


