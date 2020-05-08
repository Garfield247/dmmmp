#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from flask import Blueprint,jsonify

form = Blueprint("form",__name__)

@form.route("/fromdb/",methods=["POST"],defaults={"desc":"从数据库添加数据表的表单"})
def from_db(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@form.route("/fromfile/",methods=["POST"],defaults={"desc":"从文件添加数据表的表单"})
def from_file(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@form.route("/migration/",methods=["POST"],defaults={"desc":"数据迁移表单"})
def migration(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@form.route("/download/",methods=["POST"],defaults={"desc":"文件下载表单"})
def download(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@form.route("/info/",methods=["GET"],defaults={"desc":"获取表单信息"})
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

@form.route("/approve/",methods=["PUT"],defaults={"desc":"表单审批"})
def fromdb(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)