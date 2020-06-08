#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import request

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
    def __public_verify(cls, user, params):
        if user == None:
            return {-1: '%s is not registered or entered wrong, please login again.'%params}

        if user.confirmed == False:
            email = user.email
            ValidationEmail().reactivate_email(user, email)
            return {-1: 'Login failed, mailbox not activated.The email reactivation link has been sent, '
                        'if you want to activate a user, please click email to activate.'}
        return


    @classmethod
    def __username_verify(cls, user):
        res = cls.__public_verify(user, 'Username')
        if res:
            return res
        return

    @classmethod
    def __email_verify(cls, user):
        res = cls.__public_verify(user, 'Mailbox')
        if res:
            return res
        return

    @classmethod
    def login_username_verify_init(cls, user):
        res = cls.__username_verify(user)
        if res:
            return res
        else:
            if user.verify_password(request.json.get('password')):
                pass
            else:
                return {-1: 'Username or password error, please login again.'}
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
                return {-1: 'Mailbox or password error, please login again.'}
            return True


class UserVerify():

    @classmethod
    def judge_superuser(cls, user):
        if not user:
            return 'Do not have a super administrator,' \
                   ' please contact the administrator to create a super administrator first.'
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