#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from flask import Blueprint,jsonify

form = Blueprint("form",__name__)

@form.route("/fromdb/",method=["POST"])
def fromdb():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@form.route("/fromfile/",method=["POST"])
def fromfile():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@form.route("/migration/",method=["POST"])
def migration():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@form.route("/download/",method=["POST"])
def download():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@form.route("/info/",method=["GET"])
def info():
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

@form.route("/approve/",method=["PUT"])
def fromdb():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)