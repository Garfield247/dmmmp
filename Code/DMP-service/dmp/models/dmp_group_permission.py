#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from dmp.extensions import db

"""用户组_权限表"""
group_permission = db.Table('dmp_group_permission',
    db.Column('dmp_group_id', db.Integer, db.ForeignKey('dmp_group.id'),comment='用户组ID'),
    db.Column('dmp_permission_id', db.Integer, db.ForeignKey('dmp_permission.id'), comment='权限ID')
)
