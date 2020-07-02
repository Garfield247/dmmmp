# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD


from flask import Blueprint, request
from dmp.utils import resp_hanlder
from dmp.models import Users
from dmp.utils.response_hanlder import resp_hanlder, RET

verifier = Blueprint("verifier", __name__)


@verifier.route("/email/", methods=["POST"], defaults={"desc": {"interface_name": "验证邮箱占用","is_permission": False,"permission_belong": None}})
def email(desc):
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        user_email_obj = Users.query.filter(Users.email == email).first()
        if user_email_obj:
            return resp_hanlder(code=1010, msg=RET.alert_code[1010], result={"exist": True})
        return resp_hanlder(code=1011, msg=RET.alert_code[1011], result={"exist": False})


@verifier.route("/username/", methods=["POST"], defaults={"desc": {"interface_name": "验证用户名占用","is_permission": False,"permission_belong": None}})
def username(desc):
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        user_obj = Users.query.filter(Users.dmp_username == username).first()
        if user_obj:
            return resp_hanlder(code=1012, msg=RET.alert_code[1012], result={"exist": True})
        return resp_hanlder(code=1013, msg=RET.alert_code[1013], result={"exist": False})


@verifier.route("/case_name/", methods=["GET"], defaults={"desc": {"interface_name": "验证案例名占用","is_permission": False,"permission_belong": None}})
def case_name(desc):
    if request.method == "GET":
        try:
            case_name_ = request.json.get("dmp_case_name")
            from dmp.models import Case
            case = Case.query.filter_by(dmp_case_name=case_name_).first()
            if case:
                return resp_hanlder(result={"exist": True, })
            else:
                return resp_hanlder(result={"exist": False, })
        except Exception as err:
            return resp_hanlder(err=err)


@verifier.route("/database_name/", methods=["GET"], defaults={"desc": {"interface_name": "验证数据库名占用","is_permission": False,"permission_belong": None}})
def database_name(desc):
    if request.method == "GET":
        try:
            database_name_ = request.json.get("dmp_database_name")
            from dmp.models import Database
            database = Database.query.filter_by(dmp_database_name=database_name_).first()
            if database:
                return resp_hanlder(result={"exist": True, })
            else:
                return resp_hanlder(result={"exist": False, })
        except Exception as err:
            return resp_hanlder(err=err)


@verifier.route("/table_name/", methods=["GET"], defaults={"desc": {"interface_name": "验证数据表名占用","is_permission": False,"permission_belong": None}})
def table_name(desc):
    if request.method == "GET":
        try:
            table_name_ = request.json.get("dmp_table_name")
            from dmp.models import DataTable
            table = DataTable.query.filter_by(dmp_data_table_name=table_name_).first()
            if table:
                return resp_hanlder(result={"exist": True, })
            else:
                return resp_hanlder(result={"exist": False, })
        except Exception as err:
            return resp_hanlder(err=err)
