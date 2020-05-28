#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from datetime import timedelta

from flask import session, current_app, request

from dmp.models import Groups
# from dmp.rbac.service.init_permission import INIT_PERMISSION
from dmp.utils.validation import ValidationEmail
from dmp.models.dmp_user import Users


class LoginVerify():
    """登录校验及用户信息保存"""

    # @classmethod
    # def __session_init(cls, user):
    #     # 初始化用户对应用户组的权限
    #     INIT_PERMISSION.permission_init(user)
    #     # 保存用户登录状态
    #     # session['is_login'] = True
    #
    #     # 设置flask的session失效时间，这里保持了与token失效时间一致，保证关闭浏览器之后在打开仍可以访问
    #     # (因为flask的session在关闭浏览器之后失效)，
    #     session.permanent = True
    #     current_app.permanent_session_lifetime = timedelta(minutes=3600)

    @classmethod
    def __login_verify(cls, user):
        if user == None:
            return {
                'status': -1,
                'msg': 'Username is not registered or entered wrong, please login again',
                'results': {}
            }

        if user.confirmed == False:
            email = user.email
            ValidationEmail().reactivate_email(user, email)
            return 'Login failed, mailbox not activated.The email reactivation link has been sent, please wait a moment'
        return

    @classmethod
    def __email_verify(cls, user):
        if user == None:
            return 'Mailbox or password entered wrong, please login again'
        if user.confirmed == False:
            email = user.email
            ValidationEmail().reactivate_email(user, email)
            return 'Login failed, mailbox not activated.The email reactivation link has been sent, please wait a moment'
        return

    @classmethod
    def login_username_verify_init(cls, user):
        res = cls.__login_verify(user)
        if res:
            return res
        else:
            if user.verify_password(request.json.get('password')):
                pass
            else:
                return {-1: 'Username or password error, please login again.'}
            # cls.__session_init(user)
            return True

    @classmethod
    def login_email_verify_init(cls, user):
        res = cls.__email_verify(user)
        if res:
            return res
        else:
            if user.verify_password(request.json.get('password')):
                pass
            else:
                return {-1: 'Username or password error, please login again.'}
            # cls.__session_init(user)
            return True


class UserVerify():

    @classmethod
    def judge_superuser(cls, user):
        if not user:
            return {
                'status': -1,
                'msg': 'Do not have a super administrator, '
                       'please contact the administrator to create a super administrator first',
                'results': {}
            }
        else:
            return

    @classmethod
    def verify_token(cls, token):
        # 验证token的有效性
        res = Users.decode_auth_token(token)
        if not isinstance(res, str):
            return True
        else:
            return res

    @classmethod
    def __total_users(cls, dmp_group_id):

        if dmp_group_id == 1:
            roots_list = Users.query.filter(Users.dmp_group_id == 1).all()
            roots_max_count = Groups.query.filter(Groups.id == 1).first().max_count
            if len(roots_list) >= roots_max_count:
                return 'The number of roots exceeds the maximum capacity of the root group. Please operate again'
        elif dmp_group_id == 2:
            teachers_list = Users.query.filter(Users.dmp_group_id == 2).all()
            teachers_max_count = Groups.query.filter(Groups.id == 2).first().max_count
            if len(teachers_list) >= teachers_max_count:
                return 'The number of teachers exceeds the maximum capacity of the teacher group. Please operate again'
        elif dmp_group_id == 3:
            students_list = Users.query.filter(Users.dmp_group_id == 3).all()
            students_max_count = Groups.query.filter(Groups.id == 3).first().max_count
            if len(students_list) >= students_max_count:
                return 'The number of students exceeds the maximum capacity of the student group. Please operate again'
        return True

    @classmethod
    def judge_count(cls, dmp_group_id):
        ret = UserVerify.__total_users(dmp_group_id)
        if isinstance(ret, str):
            return (-1, ret)
        else:
            return ret
