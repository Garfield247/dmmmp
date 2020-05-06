#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from flask import Blueprint,jsonify

database = Blueprint("database",__name__)

@database.route("/info/",methods=["GET"])
def info():
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

@database.route("/del/",methods=["DEL"])
def dbdel():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@database.route("/connect/",methods=["POST"])
def connect():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@database.route("/post/",methods=["POST"])
def post():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)