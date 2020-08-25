#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/19
# @Author  : SHTD

import datetime
from dmp.extensions import db
from dmp.models import DMPModel


class Dashboard(db.Model, DMPModel):
    """数据看板表"""
    __tablename__ = 'dmp_dashboard'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, comment='看板ID')
    dmp_dashboard_name = db.Column(
        db.String(64), unique=True, nullable=False, comment='数据看板名称')
    description = db.Column(db.String(512), default=None, comment='备注,简介')
    release = db.Column(db.Integer, default=0, comment='是否发布，0否1是2下线')
    charts_position = db.Column(db.Text, comment='图标布局数据')
    upper_dmp_dashboard_archive_id = db.Column(db.Integer, comment='文件夹ID')

    created_dmp_user_id = db.Column(db.Integer, nullable=False, comment='创建人')
    changed_dmp_user_id = db.Column(db.Integer, comment='修改人')
    created_on = db.Column(
        db.DateTime, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, comment='最后修改时间')

    @classmethod
    def exsit_dashboard_by_name(cls, dashboard_name):
        item = cls.query.filter_by(dmp_dashboard_name=dashboard_name).first()
        if item:
            return True
        return False

    def delete(self):
        from .dmp_chart import Chart
        db.session.query(Chart).filter(
            Chart.dmp_dashboard_id == self.id).delete()
        db.session.delete(self)
        db.session.commit()

    @property
    def upper_dmp_dashboard_archive_name(self):

        from .dmp_archive import DashboardArchive
        if self.upper_dmp_dashboard_archive_id > 0:
            if DashboardArchive.exist_item_by_id(self.upper_dmp_dashboard_archive_id):
                archive_name = DashboardArchive.get(
                    self.upper_dmp_dashboard_archive_id).dashboard_archive_name
                return archive_name

        return "-"

    @property
    def _json_tmp(self):
        _d = {
            "created_dmp_user_name": self.created_dmp_user_name,
            "changed_dmp_user_name": self.changed_dmp_user_name,
            "upper_dmp_dashboard_archive_name": upper_dmp_dashboard_archive_name,
        }
        return _d
