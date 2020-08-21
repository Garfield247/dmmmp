#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

from dmp.extensions import db
from dmp.models import DMPModel


class ArchiveStar(db.Model, DMPModel):
    """文件夹用户收藏关联表"""
    __tablename__ = 'dmp_archive_star'
    dmp_user_id = db.Column(db.Integer, nullable=False, comment='用户ID')
    dmp_archive_id = db.Column(db.Integer, nullable=False, comment='文件夹ID')