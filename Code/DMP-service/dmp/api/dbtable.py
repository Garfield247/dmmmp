#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from flask import Blueprint,jsonify

dbtable = Blueprint("dbtable",__name__)

@dbtable.route("/info/",methods=["GET"],defaults={"desc":"获取数据表信息"})
def info(desc):
    result = {
 "status": 0,
  "msg": "ok",
  "results":[
        {
        "id":1,
        "data_table_name":"zhiliandata",
        "db_table_name":"zhanlian_data",
        "dmp_database_id":"01",
        "dmp_datebase_name":"main",
        "db_type":1,
        "dmp_case_id":"10",
        "user_id":"124",
        "description":"test",
        "created_on":"2020-03-18 15:00:00",
        "changed_on":"2020-03-28 15:00:00",
        },{
        "id":1,
        "data_table_name":"zhiliandata",
        "db_table_name":"zhanlian_data",
        "dmp_database_id":1,
        "dmp_datebase_name":"main",
        "db_type":1,
        "dmp_case_id":10,
        "user_id":123,
        "description":"test",
        "created_on":"2020-03-18 15:00:00",
        "changed_on":"2020-03-28 15:00:00",
        }
        ]
        }
    return jsonify(result)

@dbtable.route("/column/",methods=["GET"],defaults={"desc":"获取数据表的列信息"})
def column(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results":[
            {"id":"",
            "dmp_data_table_id":"",
            "dmp_data_table_column_name":"job_name",
            "groupby":"",
            "wherein":"",
            "isdate":"",
            "description":"zhiweimingcheng",}
        ]
        }

    return jsonify(result)

@dbtable.route("/columnsetting/",methods=["POST"],defaults={"desc":"数据表的数据列设置"})
def columnsetting(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@dbtable.route("/del/",methods=["DEL"],defaults={"desc":"删除数据表"})
def dbtdel(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)