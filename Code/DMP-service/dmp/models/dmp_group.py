#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

import datetime
from dmp.extensions import db
from .dmp_group_permission import group_permission
from .dmp_group_rights import group_rights

class Groups(db.Model):
    """用户组表"""
    __tablename__ = 'dmp_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户组ID')
    dmp_group_name = db.Column(db.String(32), unique=True, nullable=False, comment='用户组名')
    max_count = db.Column(db.Integer, comment='最大用户数量')
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')

    permissions = db.relationship('Permissions', secondary=group_permission)
    rights = db.relationship('Rights', secondary=group_rights)

    def __repr__(self):
        return self.dmp_group_name

    def group_to_dict(self):
        group_dict = {
            'id': self.id,
            'dmp_group_name': self.dmp_group_name,
            'max_count': self.max_count,
            'created_on': self.created_on,
            'changed_on': self.changed_on,
        }
        return group_dict