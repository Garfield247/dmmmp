# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD


from flask import Blueprint, request
from dmp.utils import resp_hanlder
from dmp.models import Users, Groups
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

@verifier.route("/dbt_name/", methods=["GET"], defaults={"desc": {"interface_name": "验证数据库表名占用","is_permission": False,"permission_belong": None}})
def db_table_name(desc):
    if request.method == "GET":
        try:
            dmp_database_id = request.json.get("dmp_database_id")
            db_table_name_ = request.json.get("db_table_name")
            from dmp.utils.engine import auto_connect
            db_ = auto_connect(dmp_database_id)
            tbl = db_.tables_list
            from dmp.models import FormMigrate,FormUpload
            count1 = FormUpload.query.filter_by(destination_db_table_name = db_table_name_).count()
            count2 = FormMigrate.query.filter_by(new_table_name = db_table_name_).count()
            if db_table_name_ in tbl or count1>0 or count2>0:
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
            from dmp.models import DataTable,FormUpload,FormAddDataTable
            count1 = DataTable.query.filter_by(dmp_data_table_name=table_name_).count()
            count2 = FormUpload.query.filter_by(dmp_data_table_name=table_name_).count()
            count3 = FormAddDataTable.query.filter_by(dmp_data_table_name=table_name_).count()
            if count1>0 or count2>0 or count3>0:
                return resp_hanlder(result={"exist": True, })
            else:
                return resp_hanlder(result={"exist": False, })
        except Exception as err:
            return resp_hanlder(err=err)


@verifier.route("/groupname/", methods=["POST"], defaults={"desc": {"interface_name": "验证用户组名占用","is_permission": False,"permission_belong": None}})
def groupname(desc):
    if request.method == 'POST':
        data = request.json
        groupname = data.get('groupname')
        group_obj = Groups.query.filter(Groups.dmp_group_name == groupname).first()
        if group_obj:
            return resp_hanlder(code=1016, msg=RET.alert_code[1016], result={"exist": True})
        return resp_hanlder(code=1017, msg=RET.alert_code[1017], result={"exist": False})


@verifier.route("/archive_name/",methods=["GET"])
def exist_archive_by_name():
    ...

@ verifier.route("/dashboard_name",methods=["GET"])
def exist_dashboard_by_name():
    ...

@verifier.route("/dataservice_name",methods=["GET"])
def exist_dataservice_by_name():
    ...

@verifier.route("/dataservice_api",methods=["GET"])
def exist_dataservice_by_api():
    ...
