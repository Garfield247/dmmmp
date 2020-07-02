#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import current_app, session

from dmp.extensions import db
from dmp.models import DMPModel


class Permissions(db.Model, DMPModel):
    """权限表"""
    __tablename__ = 'dmp_permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='权限ID')
    route = db.Column(db.String(64), nullable=False, comment='权限路由')
    dmp_permission_name = db.Column(db.String(32), nullable=False, comment='路由功能名称')

    def __repr__(self):
        return self.dmp_permission_name

    def permission_to_dict(self):
        permission_dict = {
            'id': self.id,
            'route': self.route,
            'dmp_permission_name': self.dmp_permission_name
        }
        return permission_dict

    @classmethod
    def init_permission(cls):
        permission_list = [{"route": r.rule, "desc": None if not r.defaults else r.defaults.get("desc")} for r in
                           current_app.url_map.__dict__.get("_rules")]
        db_permission_list = []
        current_app.logger.info(permission_list)
        # 将is_permission=None的接口和{'route': '/static/<path:filename>'}、
        # {'route': '/user/DMP-service/<path:filename>', 'desc': None}这两个接口剔除
        try:
            for rout in permission_list:
                current_app.logger.info(rout)
                child_rout = rout.get('desc')
                if rout.get('desc') == None or child_rout.get('is_permission') == False:
                    continue
                permission = Permissions()
                permission.route = str(rout.get("route"))
                desc_dict = rout.get('desc')
                permission.dmp_permission_name = str(desc_dict.get("interface_name"))
                db_permission_list.append(rout)
                db.session.add(permission)
            # db.session.commit()
            session['db_permission_list'] = db_permission_list
            current_app.logger.info("permission init complete")
        except Exception as err:
            current_app.logger.error(err)
