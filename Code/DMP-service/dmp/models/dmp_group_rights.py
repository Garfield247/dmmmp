#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from dmp.extensions import db

class GroupRights(db.Model):
    """用户组权利表"""
    __tablename__ = 'dmp_group_rights'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_rights_id = db.Column(db.Integer, db.ForeignKey('dmp_rights.id'), nullable=False, comment='权限ID')
    dmp_group_id = db.Column(db.Integer, db.ForeignKey('dmp_group.id'), nullable=False, comment='用户组ID')
