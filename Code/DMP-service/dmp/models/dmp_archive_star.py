#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

import datetime
from dmp.extensions import db
from dmp.models import DMPModel


class ArchiveStar(db.Model, DMPModel):
    """文件夹用户收藏关联表"""
    __tablename__ = 'dmp_archive_star'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, comment='看板ID')
    dmp_user_id = db.Column(db.Integer, nullable=False, comment='用户ID')
    dmp_archive_id = db.Column(db.Integer, nullable=False, comment='文件夹ID')

