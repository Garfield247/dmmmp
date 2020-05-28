#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from dmp.utils.email import EmailBody, send_mail


class ValidationEmail():

    def __init__(self):
        # self.confirm_url = 'http://localhost:7789/user/activate/'
        # self.change_pwd_url = 'http://localhost:7789/user/changepwd/'
        # self.gettoken_url = 'http://localhost:7789/user/gettoken/'
        self.confirm_url = 'http://192.168.26.2:8080/forget?sign=activation&token='
        self.reset_url = 'http://192.168.26.2:8080/forget?token='

    def activate_email(self, user, email):
        token = user.encode_auth_token().decode('utf-8')
        confirm_url = self.confirm_url + token
        text_body, html_body = EmailBody.email_body(user.dmp_username, confirm_url)
        # if text_body == False and html_body == False:
        #     return {-1: 'The mailbox has been activated. Please do not reactivate it'}
        send_mail.apply_async(args=[email, '账户激活', text_body, html_body])

    def reactivate_email(self, user, email):
        token = user.encode_auth_token().decode('utf-8')
        confirm_url = self.confirm_url + token
        text_body, html_body = EmailBody.resend_email(user.email, confirm_url)
        send_mail.apply_async(args=[email, '重新激活账户', text_body, html_body])

    def change_pwd(self, user, email):
        # token = user.generate_activate_token().decode('utf-8')
        # change_pwd_url = self.change_pwd_url + token
        token = user.encode_auth_token().decode('utf-8')
        confirm_url = self.reset_url + token
        text_body, html_body = EmailBody.change_pwd(user.email, confirm_url)
        send_mail.apply_async(args=[email, '重置密码', text_body, html_body])
