#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import Blueprint, jsonify, request, current_app
from dmp.models import FromUpload,FromMigrate,FromDownload,FromAddDataTable
from dmp.utils import resp_hanlder

form = Blueprint("form",__name__)

@form.route("/formdb/",methods=["POST"],defaults={"desc":"从数据库添加数据表的表单"})
def from_db(desc):
    if request.method == "POST":
        try:
            form_info = request.json
            data_tablename = form_info.get("data_tablename")
            db_tablename = form_info.get("db_tablename")
            database_id = form_info.get("database_id")
            dmp_data_case_id = form_info.get("dmp_data_case_id")
            description = form_info.get("description")
            submit_dmp_user_id = 3
            new_form = FromAddDataTable(
                dmp_data_table_name = data_tablename,
                db_table_name = db_tablename,
                dmp_database_id = database_id,
                dmp_case_id = dmp_data_case_id,
                description = description,
                submit_dmp_user_id = submit_dmp_user_id,
                )
            new_form.add()
            current_app.logger.info(new_form.id)
            return resp_hanlder(result="OK")
        except Exception as err:
            return resp_hanlder(code=999,err=err)


@form.route("/formfile/",methods=["POST"],defaults={"desc":"从文件添加数据表的表单"})
def from_file(desc):
    if request.method == "POST":
        try:
            form_info = request.json
            filetype = form_info.get("filetype")
            filepath = form_info.get("filepath")
            column_line = form_info.get("column_line")
            column = form_info.get("column")
            json_dimension_reduction = form_info.get("json_dimension_reduction")
            destination_dmp_datebase_id = form_info.get("destination_dmp_datebase_id")
            tablename = form_info.get("tablename")
            method = form_info.get("method")
            dmp_data_case_id = form_info.get("dmp_data_case_id")
            description = form_info.get("description")
            submit_dmp_user_id = 3
            new_form = FromUpload(
                filetype = filetype,
                filepath = filepath,
                column_line = column_line,
                column = column,
                json_dimension_reduction = json_dimension_reduction,
                destination_dmp_datebase_id = destination_dmp_datebase_id,
                new_tablename = tablename,
                method = method,
                dmp_data_case_id = dmp_data_case_id,
                description = description,
                submit_dmp_user_id = submit_dmp_user_id,
                )
            new_form.add()
            current_app.logger.info(new_form.id)
            return resp_hanlder(result="OK")
        except Exception as err:
            return resp_hanlder(code=999,err=err)

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
