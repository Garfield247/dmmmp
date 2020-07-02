#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import request

from dmp.utils.validation import ValidationEmail
from dmp.models.dmp_user import Users


class LoginVerify():
    """登录校验及用户信息保存"""

    @classmethod
    def __public_verify(cls, user, params):
        if user == None:
            return {-1: '%s is not registered or entered wrong, please login again.'%params}

        if user.confirmed == False:
            # email = user.email
            # ValidationEmail().reactivate_email(user, email)
            return {-1: 'Login failed, The message is not activated,'
                        ' please contact your administrator to activate it'}
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