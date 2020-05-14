#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

import time
import datetime
<<<<<<< HEAD
from faker import Faker
from flask import current_app
from itsdangerous import Serializer, BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from dmp.models import DMPModel
=======

from flask import current_app, flash, jsonify

>>>>>>> 86cec918be112616cf9c9d2bd61ae808ed8b2538
from dmp.extensions import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired


class Users(db.Model,DMPModel):
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

<<<<<<< HEAD
    # groups = db.relationship('Groups', backref='users')
    # leader = db.relationship('Users', backref='leader')

    @property
    def password(self):
        """密码保护"""
        raise AttributeError('密码是不可读属性')

    @password.setter
    def password(self,password):
        """设置密码，加密存储"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        """密码校验"""
        return check_password_hash(self.password_hash,password)


    def generate_activate_token(self, expires_in=3600):
        """生成激活的token 到期时间为3600秒"""
        # 创建用于生成token的类，需要传递秘钥和有效期
        s = Serializer(current_app.config['SECRET_KEY'], expires_in)
        # 生成包含有效信息(必须是字典数据)的token字符串
        return s.dumps({'id': self.id})

    def generate_newmailactivate_token(self,newmail, expires_in=3600):
        """生成修改邮箱的token 到期时间为3600秒"""
        # 创建用于生成token的类，需要传递秘钥和有效期
        s = Serializer(current_app.config['SECRET_KEY'], expires_in)
        # 生成包含有效信息(必须是字典数据)的token字符串
        return s.dumps({'id': self.id,'newmail':newmail})


    @staticmethod
    def check_activate_token(token):
        """用户激活"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # 解析token
            data = s.loads(token)
        except BadSignature:
            return False
        except SignatureExpired:
            return False
        user = Users.query.get(data.get('id'))
        if not user:
            return False
        # 没有激活才需要激活
        if not user.confirmed:
            user.confirmed = True
        db.session.add(user)
        return True

    # 邮箱修改确认
    @staticmethod
    def check_newmailactivate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)   #解析token
        except BadSignature:
            return False
        except SignatureExpired:
            return False
        user = Users.query.get(data.get('id'))
        if not user:
            return False
        user.email = data.get('newmail')
        return True

    @classmethod
    def user_init(cls):
        """初始化管理员用户"""
        pass

    @classmethod
    def create_test_user(cls):
        test_user = {
            "admin_test":1,
            "teacher_test":2,
            "student_test":3
        }
        for k,v in test_user.items():
            user = Users()
            user.dmp_username = k
            user.real_name = k
            user.email = "%s@test.com"%k
            user.passwd = "123456"
            user.confirmed = True
            user.dmp_group_id = k
            db.session.add(user)
        db.session.commit()
        current_app.logger.info("create test user complete!")


=======
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
>>>>>>> 86cec918be112616cf9c9d2bd61ae808ed8b2538
