  
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from flask import Blueprint, jsonify, request
from dmp.models import Users

verifier = Blueprint("verifier",__name__)

@verifier.route("/email/",methods=["POST"],defaults={"desc":"验证邮箱占用"})
def email(desc):
    email = request.form.get('email')
    user_email_obj = Users.query.filter(Users.email == email).first()
    if user_email_obj:
        result = {
            "status": -1,
            "msg": "Mailbox has been used, you should change the mailbox!",
            "results": {
                "exist": True,
            }
        }
        return jsonify(result)
    result = {
        "status": 0,
        "msg": "Mailbox can be used, you can use it!",
        "results": {
            "exist": False,
        }
    }
    return jsonify(result)

@verifier.route("/username/", methods=["POST"],defaults={"desc":"验证用户名占用"})
def username(desc):
    username = request.form.get('username')
    user_obj = Users.query.filter(Users.dmp_username==username).first()
    if user_obj:
        result = {
            "status": -1,
            "msg": "Username has been used, you should change the username!",
            "results": {
                "exist": True,
            }
        }
        return jsonify(result)
    result = {
        "status": 0,
        "msg": "Username can be used, you can use it!",
        "results": {
            "exist": False,
        }
    }
    return jsonify(result)