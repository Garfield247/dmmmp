#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

import time
import datetime
from faker import Faker
from dmp.extensions import db


class Users(db.Model):
    """用户表"""
    __tablename__ = 'dmp_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    dmp_username = db.Column(db.String(32), unique=True, nullable=False, comment='用户名')
    real_name = db.Column(db.String(32), nullable=False, comment='真实姓名')
    email = db.Column(db.String(32), unique=True, nullable=False, comment='用户邮箱')
    passwd = db.Column(db.String(64), nullable=False, comment='用户密码，加密储存')
    confirmed = db.Column(db.Boolean, default=False, comment='用户激活状态')
    icon = db.Column(db.String(128), default=None, comment='用户头像')
    dmp_user_info = db.Column(db.String(256), default=None, comment='个人简介')
    last_login = db.Column(db.DateTime, default=datetime.datetime.now, comment='最后登录时间')
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    dmp_group_id = db.Column(db.Integer, db.ForeignKey('dmp_group.id'), nullable=False, comment='所属用户组ID，默认学生用户组')
    leader_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), comment='直属管理者，默认是超级管理员用户, 自关联')

    groups = db.relationship('Groups', backref='users')
    leader = db.relationship('Users', backref='leader')

    @classmethod
    def user_init(cls):
        """初始化管理员用户"""
        f = Faker("zh_CN")


        pass
    @classmethod
    def create_test_data(cls):
        pass
