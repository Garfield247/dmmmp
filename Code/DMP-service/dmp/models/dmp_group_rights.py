#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from dmp.extensions import db

"""用户组权利表"""
group_rights = db.Table('dmp_group_rights',
                        db.Column('dmp_group_id', db.Integer, db.ForeignKey('dmp_group.id'), comment='用户组ID'),
                        db.Column('dmp_rights_id', db.Integer, db.ForeignKey('dmp_rights.id'), comment='权利ID')
                        )
