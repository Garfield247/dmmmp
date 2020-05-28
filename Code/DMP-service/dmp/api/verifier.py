# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import Blueprint, request

from dmp.models import Users
from dmp.utils.response_hanlder import resp_hanlder, RET

verifier = Blueprint("verifier", __name__)


@verifier.route("/email/", methods=["POST"], defaults={"desc": "验证邮箱占用"})
def email(desc):
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        user_email_obj = Users.query.filter(Users.email == email).first()
        if user_email_obj:
            return resp_hanlder(code=1010, msg=RET.alert_code[1010], result={"exist": True})
        return resp_hanlder(code=1011, msg=RET.alert_code[1011], result={"exist": False})


@verifier.route("/username/", methods=["POST"], defaults={"desc": "验证用户名占用"})
def username(desc):
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        user_obj = Users.query.filter(Users.dmp_username == username).first()
        if user_obj:
            return resp_hanlder(code=1012, msg=RET.alert_code[1012], result={"exist": True})
        return resp_hanlder(code=1013, msg=RET.alert_code[1013], result={"exist": False})
