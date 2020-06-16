#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

import datetime
import jwt

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from dmp.models import DMPModel
from dmp.extensions import db
from dmp.utils.response_hanlder import resp_hanlder, RET


class Users(db.Model, DMPModel):
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

    def encode_auth_token(self):
        '''用户登录后，发放有效的 JWT'''
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60*60*24),
                'iat': datetime.datetime.utcnow(),
                'user_id': self.id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token):
        '''验证 JWT 的有效性'''
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def check_activate_token(res):
        # 激活邮箱
        try:
            user = Users.query.get(res.get('id'))
            if not user:
                return resp_hanlder(code=1008, msg=RET.alert_code[1008], result={})
            if not user.confirmed:
                user.confirmed = True
                db.session.add(user)
                db.session.commit()
            return True
        except Exception as err:
            return resp_hanlder(code=999, err=err)

    @classmethod
    def reset_password(cls, token, new_password):
        res = cls.decode_auth_token(token)
        if not isinstance(res, str):
            user = Users.query.filter(Users.id == res).first()
            user.password = new_password
            db.session.add(user)
            db.session.commit()
            return True
        else:
            return res

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.passwd = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码"""
        return check_password_hash(self.passwd, password)

    # # 邮箱修改确认
    # @staticmethod
    # def check_newmailactivate_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)  # 解析token
    #     except BadSignature:
    #         return False
    #     except SignatureExpired:
    #         return False
    #     user = Users.query.get(data.get('id'))
    #     if not user:
    #         return False
    #     user.email = data.get('newmail')
    #     return True
