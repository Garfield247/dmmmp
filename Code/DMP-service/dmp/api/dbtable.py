#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD


from flask import Blueprint, jsonify, request, current_app
from dmp.models import Case,DataTable
from dmp.utils import resp_hanlder


dbtable = Blueprint("dbtable",__name__)

@dbtable.route("/info/",methods=["GET"],defaults={"desc":"获取数据表信息"})
def info(desc):
    if request.method == "GET":
        try:
            dmp_data_table_id = request.json.get("dmp_data_table_id")
            dmp_case_id = request.json.get("dmp_case_id")
            if dmp_case_id and not dmp_data_table_id:
                dbtables =[dtb.__json__() for dtb in DataTable.query.filter_by(dmp_case_id=dmp_case_id).all()]
                current_app.logger.info(dbtables)
                return  resp_hanlder(result=dbtables)
            elif dmp_data_table_id and not dmp_case_id:
                db_table = DataTable.get(dmp_data_table_id).__json__()
                current_app.logger.info(db_table)
                return  resp_hanlder(result=db_table)
        except Exception as err:
            return  resp_hanlder(err=err)

def post(dmp_data_table_name,
        db_table_name,
        description,
        dmp_user_id,
        dmp_database_id,
        dmp_case_id):
    """添加数据表"""
    new_db_table = DataTable(
        dmp_data_table_name = dmp_data_table_name,
        db_table_name = db_table_name,
        description = description,
        dmp_user_id = dmp_user_id,
        dmp_database_id = dmp_database_id,
        dmp_case_id = dmp_case_id)
    new_db_table.save()
    return new_db_table.__json__()


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
