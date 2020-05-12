#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

import datetime

from flask import current_app, flash, jsonify

from dmp.extensions import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired


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
    leader = db.relationship('Users', remote_side=[id], backref='selfleader')

    def __repr__(self):
        return self.dmp_username

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)
        if self.dmp_group_id is None:
            self.dmp_group_id = 3

    def user_to_dict(self):
        user_dict = {
            'id': self.id,
            'dmp_username': self.dmp_username,
            'real_name': self.real_name,
            'email': self.email,
            'passwd': self.passwd,
            'confirmed': self.confirmed,
            'icon': self.icon,
            'dmp_user_info': self.dmp_user_info,
            'last_login': self.last_login,
            'created_on': self.created_on,
            'changed_on': self.changed_on,
            'dmp_group_id': self.dmp_group_id,
            'leader_dmp_user_id': self.leader_dmp_user_id,
        }
        return user_dict

    def generate_activate_token(self, expires_in=3600):   #到期时间为3600秒
        s = Serializer(current_app.config['SECRET_KEY'], expires_in)
        return s.dumps({'id': self.id})

    # 账户激活，因为激活时还不知道是哪个用户
    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except BadSignature:
            return jsonify({
                'status': 201,
                'msg': 'Useless token, please resend it again',
                'results': {}
            })
        except SignatureExpired:
            return jsonify({
                'status': 201,
                'msg': 'Token have lost effectiveness, please resend it again',
                'results': {}
            })
        user = Users.query.get(data.get('id'))
        if not user:
            return jsonify({
                'status': -1,
                'msg': 'The activated account does not exist',
                'results': {}
            })
        if not user.confirmed:
            user.confirmed = True
            db.session.add(user)
        return True

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except BadSignature:
            return jsonify({
                'status': 201,
                'msg': 'Useless token, please resend it again',
                'results': {}
            })
        except SignatureExpired:
            return jsonify({
                'status': 201,
                'msg': 'Token have lost effectiveness, please resend it again',
                'results': {}
            })
        user = Users.query.get(data.get('id'))  # 当查询条件为模型的主键时，可以直接用get进行查询，拿到对应的User模型
        user.passwd = new_password
        db.session.add(user)
        return True