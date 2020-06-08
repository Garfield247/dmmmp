 # !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import Blueprint, jsonify, request
from dmp.utils import resp_hanlder
from dmp.models import Users

verifier = Blueprint("verifier", __name__)


@verifier.route("/email/", methods=["POST"], defaults={"desc": "验证邮箱占用"})
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


@verifier.route("/username/", methods=["POST"], defaults={"desc": "验证用户名占用"})
def username(desc):
    username = request.form.get('username')
    user_obj = Users.query.filter(Users.dmp_username == username).first()
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


# @verifier.route("/case_name/", methods=["GET"],defaults={"desc": "验证案例名占用"})
# def case_name(desc):
#     if request.method == "GET":
#         try:
#             case_name_ = request.json.get("dmp_case_name")
#             from dmp.models import Case
#             case = Case.query.filter_by(dmp_case_name = case_name_)
#             if case:
#                 return resp_hanlder(result={"exist": True, })
#             else:
#                 return resp_hanlder(result={"exist": False, })


# @verifier.route("/database_name/", methods=["GET"], defaults={"desc": "验证数据库名占用"})
# def database_name(desc):
#     if request.method == "GET":
#         try:
#             database_name_ = request.json.get("dmp_database_name")
#             from dmp.models import Database
#             database = Database.query.filter_by(dmp_database_name=database_name_)
#             if database:
#                 return resp_hanlder(result={"exist": True, })
#             else:
#                 return resp_hanlder(result={"exist": False, })


# @verifier.route("/table_name/", methods=["GET"], defaults={"desc": "验证数据库名占用"})
# def table_name(desc):
#     if request.method == "GET":
#         try:
#             table_name_ = request.json.get("dmp_table_name")
#             from dmp.models import DataTable
#             table = DataTable.query.filter_by(dmp_data_table_name=table_name_)
#             if table:
#                 return resp_hanlder(result={"exist": True, })
#             else:
#                 return resp_hanlder(result={"exist": False, })
