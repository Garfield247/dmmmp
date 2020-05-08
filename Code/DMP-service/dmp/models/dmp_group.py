#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

import datetime
from flask import current_app
from dmp.extensions import db
from .dmp_group_permission import group_permission
from .dmp_group_rights import group_rights

class Group(db.Model):
    """用户组表"""
    __tablename__ = 'dmp_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户组ID')
    dmp_group_name = db.Column(db.String(32), unique=True, nullable=False, comment='用户组名')
    max_count = db.Column(db.Integer, comment='最大用户数量')
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')

    permissions = db.relationship('Permissions', secondary=group_permission)
    # rights = db.relationship('Rights', secondary=group_rights)

    @classmethod
    def init_group(cls):
        try:
            from .dmp_permission import Permissions
            admin_group = Group()
            admin_group.dmp_group_name = "admin"
            admin_group.max_count = 3
            current_app.logger.info(Permissions.query.all())
            db.session.add(admin_group)
            db.session.commit()
            for per in Permissions.query.all():
                admin_group.permissions.append(per)
            db.session.commit()

            current_app.logger.info("create admin group")

        except Exception as err:
            current_app.logger.error(err)

