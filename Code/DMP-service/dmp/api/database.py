#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from flask import Blueprint, jsonify, request

database = Blueprint("database",__name__)

@database.route("/info/",methods=["GET"],defaults={"desc":"数据库信息"})
def info(desc):
    result = {
 "status": 0,
  "msg": "ok",
  "results":[
        {
        "id":1,
        "dmp_datebase_name":"main",
        "dmp_user_id":1,
        "db_type":1,
        "db_host":"192.168.3.221",
        "db_port":"3306",
        "db_name":"dmp",
        "description":"主数据库HIVE数据库",
        "created_on":"2020-03-18 15:00:00",
        "changed_on":"2020-03-28 15:00:00",
        },
        {
        "id":3,
        "dmp_datebase_name":"test_mysql",
        "dmp_user_id":12,
        "db_type":2,
        "db_host":"192.168.3.221",
        "db_port":"3306",
        "db_name":"dmp",
        "description":"测试使用的mysql数据库",
        "created_on":"2020-03-18 15:00:00",
        "changed_on":"2020-03-28 15:00:00",
        }
        ]
        }
    return jsonify(result)

@database.route("/del/",methods=["DEL"],defaults={"desc":"删除数据库连接信息"})
def dbdel(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@database.route("/connect/",methods=["POST"],defaults={"desc":"测试数据库连接"})
def connect(desc):
    if request.method == "POST":
        db_info = request.josn
        db_type = db_info.get("db_type")
        if db_type == 1:
            pass
        result = {
            "status": 0,
            "msg": "ok",
            "results": {
            }
        }
    return jsonify(result)

@database.route("/post/",methods=["POST"],defaults={"desc":"添加/修改数据库信息"})
def post(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)