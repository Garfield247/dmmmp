#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import Blueprint, jsonify, request, current_app
from dmp.models import FromUpload,FromMigrate,FromDownload,FromAddDataTable,Users
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

    if request.method == "POST":
        try:
            form_info = request.json
            origin_dmp_table_id = form_info.get("origin_dmp_table_id")
            rule = form_info.get("rule")
            destination_dmp_datebase_id = form_info.get("destination_dmp_datebase_id")
            new_table_name = form_info.get("new_table_name")
            method = form_info.get("method")
            description = form_info.get("description")
            submit_dmp_user_id = 3
            new_form = FromMigrate(
                origin_dmp_table_id = origin_dmp_table_id,
                rule = rule,
                destination_dmp_datebase_id = destination_dmp_datebase_id,
                new_table_name = new_table_name,
                method = method,
                description = description,
                submit_dmp_user_id = submit_dmp_user_id,
                )
            new_form.add()
            current_app.logger.info(new_form.id)
            return resp_hanlder(result="OK")
        except Exception as err:
            return resp_hanlder(code=999,err=err)

@form.route("/download/",methods=["POST"],defaults={"desc":"文件下载表单"})
def download(desc):

    if request.method == "POST":
        try:
            form_info = request.json
            dmp_table_id = form_info.get("dmp_table_id")
            rule = form_info.get("rule")
            destination_dmp_datebase_id = form_info.get("destination_dmp_datebase_id")
            description = form_info.get("description")
            submit_dmp_user_id = 3
            new_form = FromDownload(
                dmp_table_id = dmp_table_id,
                rule = rule,
                destination_dmp_datebase_id = destination_dmp_datebase_id,
                description = description,
                submit_dmp_user_id = submit_dmp_user_id,
                )
            new_form.add()
            current_app.logger.info(new_form.id)
            return resp_hanlder(result="OK")
        except Exception as err:
            return resp_hanlder(code=999,err=err)

def form_permission(user_id):
    pass

@form.route("/info/",methods=["GET"],defaults={"desc":"获取表单信息"})
def info(desc):
    if request.method == "GET":
        forms = [FromAddDataTable,FromUpload,FromMigrate,FromDownload,]
        user_id = 1
        try:
            committed,pending,complete = [],[],[]
            if form_permission(user_id) == 1:
                for _form in forms:
                    committed.append([f.__json__() for f in _form.query.filter_by(submit_dmp_user_id=user_id,approve_result=0).all()])
                    complete.append([f.__json__() for f in _form.query.filter(_form.submit_dmp_user_id==user_id,_form.approve_result!=0).all()])
                resp_hanlder(result={"comiitted":committed,"complete":complete})
            if form_permission(user_id) == 2:
                for _form in forms:
                    committed.append([f.__json__() for f in _form.query.filter_by(submit_dmp_user_id=user_id,approve_result=0).all()])
                    pending.append([f.__json__()  for f in _form.query.filter_by(submit_dmp_user_id=u.id,approve_result=0).all() for u in Users.query.filter_by(leader_dmp_user_id=user_id).all()] )
                    complete.append([f.__json__() for f in _form.query.filter(_form.submit_dmp_user_id==user_id or _form.approve_dmp_user_id==user_id,_form.approve_result!=0).all()])
                resp_hanlder(result={"comiitted":committed,"pending":pending,"complete":complete})
            if form_permission(user_id) == 3:
                for _form in forms:
                    pending.append([f.__json__()  for f in _form.query.filter_by(approve_result=0).all() ] )
                    complete.append([f.__json__() for f in _form.query.filter(_form.approve_result!=0).all()])
                resp_hanlder(result={"pending":p,"complete":complete})
        except Exception as err:
            resp_hanlder(code=999,err=err)



@form.route("/approve/",methods=["PUT"],defaults={"desc":"表单审批"})
def approve(desc):
    if request.method == "PUT":
        try:
            approve_form_info = request.json
            form_type = approve_form_info.get("dmp_form_type")
            if form_type == 1:
                # 从数据库添加数据表单
                pass
            elif form_type == 2:
                # 文件上传添加数据表单
                pass
            elif form_type == 3:
                # 数据迁移表单
                pass
            elif form_type == 4:
                # 数据下载表单
                pass
        except Exception as err:
            return resp_hanlder(code=999,err=err)
