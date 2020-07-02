#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

import datetime

from flask import current_app, session

from dmp.extensions import db
from .dmp_group_permission import group_permission
from dmp.models import DMPModel


class Groups(db.Model, DMPModel):
    """用户组表"""
    __tablename__ = 'dmp_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户组ID')
    dmp_group_name = db.Column(db.String(32), unique=True, nullable=False, comment='用户组名')
    # max_count = db.Column(db.Integer, comment='最大用户数量')
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')

    permissions = db.relationship('Permissions', secondary=group_permission)

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

    @classmethod
    def init_group(cls):
        try:
            from .dmp_permission import Permissions
            admin_group = Groups()
            admin_group.dmp_group_name = "admin"
            current_app.logger.info(Permissions.query.all())
            db.session.add(admin_group)
            db.session.commit()
            for per in Permissions.query.all():
                admin_group.permissions.append(per)
            db.session.commit()
            current_app.logger.info("create admin group")

            teacher_group = Groups()
            teacher_group.dmp_group_name = "teacher"
            db.session.add(teacher_group)
            db.session.commit()
            # 默认给教师分配权限
            db_permission_list = session.get('db_permission_list')
            for rout in db_permission_list:
                desc_dict = rout.get('desc')
                # 1:为教师拥有的权限
                if desc_dict.get('permission_belong') == 0 or desc_dict.get('permission_belong') == 1:
                    teacher_group.permissions.append(Permissions.query.filter(
                            Permissions.dmp_permission_name == desc_dict.get('interface_name')).first())
            current_app.logger.info("create teacher group")

            student_group = Groups()
            student_group.dmp_group_name = "student"
            db.session.add(student_group)
            db.session.commit()
            # 默认给学生分配权限
            for rout in db_permission_list:
                desc_dict = rout.get('desc')
                # 0:为学生拥有的权限(同时教师也拥有)
                if desc_dict.get('permission_belong') == 0:
                    student_group.permissions.append(Permissions.query.filter(
                            Permissions.dmp_permission_name == desc_dict.get('interface_name')).first())
            current_app.logger.info("create student group")

        except Exception as err:
            current_app.logger.error(err)
