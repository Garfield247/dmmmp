#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/19
# @Author  : SHTD

from dmp.extensions import db
from dmp.models import DMPModel


class DashboardArchive(db.Model, DMPModel):
    """数据看板文件夹表"""
    __tablename__ = 'dmp_dashboard_archive'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, comment='看板ID')
    dashboard_archive_name = db.Column(
        db.String(64), unique=True, nullable=False, comment='文件夹名称')
    upper_dmp_dashboard_archive_id = db.Column(
        db.Integer, default=0, comment='文件夹ID')

    created_dmp_user_id = db.Column(db.Integer, nullable=False, comment='创建人')
    changed_dmp_user_id = db.Column(db.Integer, comment='修改人')
    created_on = db.Column(
        db.DateTime, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, comment='最后修改时间')

    @classmethod
    def exsit_archive_by_name(cls, archive_name):
        item = cls.query.filter_by(dashboard_archive_name=archive_name).first()
        if item:
            return True
        return False

    def delete(self):
        form .dmp_dashboard import Dashboard
        db.session.query(Dashboard).filter(Dashboard.upper_dmp_dashboard_archive_id=self.id).delete()
        db.session.delete(self)
        db.session.commit()

    @property
    def upper_dmp_dashboard_archive_name(self):

        if self.upper_dmp_dashboard_archive_id > 0:
            if self.exist_item_by_id(self.upper_dmp_dashboard_archive_id):
                archive_name = DashboardArchive.get(
                    self.upper_dmp_dashboard_archive_id).dashboard_archive_name
                return archive_name

        return "-"
