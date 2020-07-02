#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from flask import Blueprint, jsonify, request

from dmp.utils import resp_hanlder

form = Blueprint("form",__name__)

# @form.route("/fromdb/",methods=["POST"],defaults={"desc":"从数据库添加数据表的表单"})
@form.route("/fromdb/",methods=["POST"], defaults={"desc": {"interface_name": "从数据库添加数据表的表单",
                                                           "is_permission": True,
                                                           "permission_belong": 0}})
def from_db(desc):
    if request.method == "POST":
        try:
            pass
        except Exception as err:
            return

# @form.route("/fromfile/",methods=["POST"],defaults={"desc":"从文件添加数据表的表单"})
@form.route("/fromfile/",methods=["POST"], defaults={"desc": {"interface_name": "从文件添加数据表的表单",
                                                             "is_permission": True,
                                                             "permission_belong": 0}})
def from_file(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

# @form.route("/migration/",methods=["POST"],defaults={"desc":"数据迁移表单"})
@form.route("/migration/",methods=["POST"], defaults={"desc": {"interface_name": "数据迁移表单",
                                                               "is_permission": True,
                                                               "permission_belong": 0}})
def migration(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

# @form.route("/download/",methods=["POST"],defaults={"desc":"文件下载表单"})
@form.route("/download/",methods=["POST"], defaults={"desc": {"interface_name": "文件下载表单",
                                                               "is_permission": True,
                                                               "permission_belong": 0}})
def download(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

# @form.route("/info/",methods=["GET"],defaults={"desc":"获取表单信息"})
@form.route("/info/",methods=["GET"], defaults={"desc": {"interface_name": "获取表单信息",
                                                         "is_permission": True,
                                                         "permission_belong": 0}})
def info(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results":{
        "committed":[
            {"id":"",
            "form_type":1,
            "submit_on":"",
            "submit_dmp_user_id":"",
            "dmp_data_table_name":"",
            "db_table_name":"",
            "dmp_database_id":"",
            "dmp_case_id":"",
            "description":"",
            "approve_dmp_user_id":"",
            "approve_on":"",
            "approve_result":"",
            "answer":"",
            "created_on":"",
            "changed_on":"",
            }
        ],
        "pending":[],
        "complete":[]
        }}

    return jsonify(result)

# @form.route("/approve/",methods=["PUT"],defaults={"desc":"表单审批"})
@form.route("/approve/",methods=["PUT"], defaults={"desc": {"interface_name": "表单审批",
                                                            "is_permission": True,
                                                            "permission_belong": 2}})
def fromdb(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)