#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from dmp.extensions import db

class GroupPermission(db.Model):
    """用户组_权限表"""
    __tablename__ = 'dmp_group_permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_group_id = db.Column(db.Integer, db.ForeignKey('dmp_group.id'), nullable=False, comment='用户组ID')
    dmp_permission_id = db.Column(db.Integer, db.ForeignKey('dmp_permission.id'), comment='权限ID')