#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import Blueprint, jsonify, request, current_app

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
        db_info = request.json
        current_app.logger.info(db_info)
        db_type = db_info.get("db_type")
        db_host = db_info.get("db_host")
        db_port = db_info.get("db_port")
        db_user = db_info.get("db_user")
        db_password = db_info.get("db_password")
        db_name = db_info.get("db_name")
        if int(db_type) == 1:
            try:
                import pymysql
                current_app.logger.info(db_host)
                conn = pymysql.connect(db_host, db_port, db_user, db_password, db_name,charset='utf8mb4')
                current_app.logger.info(conn.server_version)
                res = {"connect":"ok!"}
            except Exception as err:
                res = {"connect":"fail!","error_message":str(err)}
        elif int(db_type) == 2:
            try:
                from pymongo import MongoClient
                conn = MongoClient(host=db_host,port=db_port,username=db_user,password=db_password)
                current_app.logger.info(conn.server_info())
                res = {"connect":"ok!"}
            except Exception as err:
                res = {"connect":"fail!","error_message":str(err)}
        elif int(db_type) == 3:
            try:
                from pyhive import hive
                conn = hive.Connection(host=db_host,port=db_port,username=db_user,password=db_password,database=db_name)
                current_app.logger.info(conn.__dict__)
            except Exception as err:
                res = {"connect":"fail!","error_message":str(err)}
        result = {
            "status": 0,
            "msg": "ok",
            "results": res
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
