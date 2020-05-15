#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from flask import current_app
from dmp.extensions import db
from dmp.models import DMPModel


class Permissions(db.Model, DMPModel):
    """权限表"""
    __tablename__ = 'dmp_permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='权限ID')
    route = db.Column(db.String(64), nullable=False, comment='权限路由')
    dmp_permission_name = db.Column(db.String(32), nullable=False, comment='路由功能名称')

    @classmethod
    def init_permission(cls):
        permission_list = [{"route": r.rule, "desc": None if not r.defaults else r.defaults.get("desc")} for r in
                           current_app.url_map.__dict__.get("_rules")]
        current_app.logger.info(permission_list)
        try:
            for rout in permission_list:
                current_app.logger.info(rout)
                permission = Permissions()
                permission.route = str(rout.get("route"))
                permission.dmp_permission_name = str(rout.get("desc"))
                db.session.add(permission)
            # db.session.commit()
            current_app.logger.info("permission init complete")
        except Exception as err:
            current_app.logger.error(err)
