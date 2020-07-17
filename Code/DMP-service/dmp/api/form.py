#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD
import datetime
import os
import socket

import pandas as pd
from flask import Blueprint, request, current_app
from sqlalchemy import or_, and_, tuple_
from sqlalchemy.sql import exists
from sqlalchemy.testing import in_

from dmp.extensions import db
from dmp.models import FormUpload, FormMigrate, FormDownload, FormAddDataTable,Forms,Users, DataTable, Database, Permissions
from dmp.utils import resp_hanlder, uuid_str
from dmp.utils.datax_job_hanlder import mysql_reader, mysql_writer, mongodb_reader, mongodb_writer, hive_reader, \
    hive_writer, textfile_reader, textfile_writer
from dmp.utils.job_task import job_hanlder
from dmp.api.dbtable import post
from dmp.utils.engine import auto_connect, hive_engine, mysql_engine, mongo_engine, create_table_query_handler

form = Blueprint("form", __name__)


@form.route("/formdb/", methods=["POST"],
            defaults={"desc": {"interface_name": "提交从数据库添加数据表的表单", "is_permission": True, "permission_belong": 0}})
def from_db(desc):
    if request.method == "POST":
        try:
            auth_token = request.headers.get('Authorization')
            submit_dmp_user_id = Users.decode_auth_token(auth_token)
            form_info = request.json
            data_tablename = form_info.get("data_tablename")
            db_tablename = form_info.get("db_tablename")
            database_id = form_info.get("database_id")
            dmp_data_case_id = form_info.get("dmp_data_case_id")
            description = form_info.get("description")
            new_form_info = FormAddDataTable(
                dmp_data_table_name=data_tablename,
                db_table_name=db_tablename,
                dmp_database_id=database_id,
                dmp_case_id=dmp_data_case_id,
            )
            new_form_info.save()
            new_form = Forms(
                submit_dmp_user_id=submit_dmp_user_id,
                description=description,
                form_info_id=new_form_info.fid
            )
            new_form.save()
            return resp_hanlder(result="OK")
        except Exception as err:
            return resp_hanlder(code=999, err=err)




@form.route("/fromfile/", methods=["POST"],
            defaults={"desc": {"interface_name": "提交从文件添加数据表的表单", "is_permission": True, "permission_belong": 0}})
def from_file(desc):
    if request.method == "POST":
        try:
            auth_token = request.headers.get('Authorization')
            submit_dmp_user_id = Users.decode_auth_token(auth_token)
            form_info = request.json
            filetype = form_info.get("filetype")
            filepath = form_info.get("filepath")
            column_line = form_info.get("column_line")
            column = form_info.get("column")
            json_dimension_reduction = form_info.get("json_dimension_reduction")
            destination_dmp_database_id = form_info.get("destination_dmp_database_id")
            destination_db_table_name = form_info.get("tablename")
            dmp_data_table_name = form_info.get("dmp_data_table_name")
            method = form_info.get("method")
            dmp_data_case_id = form_info.get("dmp_data_case_id")
            description = form_info.get("description")
            new_form_info = FormUpload(
                filetype=filetype,
                filepath=filepath,
                column_line=column_line,
                column=column,
                destination_dmp_database_id=destination_dmp_database_id,
                destination_db_table_name=destination_db_table_name,
                dmp_data_table_name=dmp_data_table_name,
                method=method,
                dmp_case_id=dmp_data_case_id,

            )
            new_form_info.save()
            new_form = Forms(
                submit_dmp_user_id=submit_dmp_user_id,
                description=description,
                form_info_id=new_form_info.fid
            )
            new_form.save()


            return resp_hanlder(result="OK")
        except Exception as err:
            return resp_hanlder(code=999, err=err)


@form.route("/migration/", methods=["POST"],
            defaults={"desc": {"interface_name": "提交数据迁移表单", "is_permission": True, "permission_belong": 0}})
def migration(desc):
    if request.method == "POST":
        try:
            auth_token = request.headers.get('Authorization')
            submit_dmp_user_id = Users.decode_auth_token(auth_token)
            form_info = request.json
            origin_dmp_table_id = form_info.get("origin_dmp_table_id")
            rule = form_info.get("rule")
            destination_dmp_database_id = form_info.get("destination_dmp_database_id")
            new_table_name = form_info.get("new_table_name")
            method = form_info.get("method")
            description = form_info.get("description")
            new_form_info = FormMigrate(
                origin_dmp_table_id=origin_dmp_table_id,
                destination_dmp_database_id=destination_dmp_database_id,
                new_table_name=new_table_name,
            )
            new_form_info.save()
            new_form = Forms(
                submit_dmp_user_id=submit_dmp_user_id,
                description=description,
                form_info_id=new_form_info.fid
            )
            new_form.save()
            current_app.logger.info(new_form.id)
            return resp_hanlder(result="OK")
        except Exception as err:
            return resp_hanlder(code=999, err=err)


@form.route("/download/", methods=["POST"],
            defaults={"desc": {"interface_name": "提交文件下载表单", "is_permission": True, "permission_belong": 0}})
def download(desc):
    if request.method == "POST":
        try:
            auth_token = request.headers.get('Authorization')
            submit_dmp_user_id = Users.decode_auth_token(auth_token)
            form_info = request.json
            dmp_data_table_id = form_info.get("dmp_data_table_id")
            rule = form_info.get("rule")
            description = form_info.get("description")
            new_form_info = FormDownload(
                dmp_data_table_id=dmp_data_table_id,
            )
            new_form_info.save()
            new_form = Forms(
                submit_dmp_user_id=submit_dmp_user_id,
                description=description,
                form_info_id=new_form_info.fid
            )
            new_form.save()
            current_app.logger.info(new_form.id)
            return resp_hanlder(result="OK")
        except Exception as err:
            return resp_hanlder(code=999, err=err)


def form_permission(user_id):
    user = Users.get(user_id)
    usergroup_id = user.groups.id
    approve_id = Permissions.query.filter_by(route="/form/approve/").first().id
    p_ids = [p.id for p in user.groups.permissions]
    if usergroup_id == 1:
        return 3
    elif approve_id in p_ids:
        return 2
    elif approve_id not in p_ids:
        return 1


@form.route("/info/", methods=["GET"],
            defaults={"desc": {"interface_name": "获取表单信息", "is_permission": True, "permission_belong": 0}})
def info(desc):
    if request.method == "GET":
        auth_token = request.headers.get('Authorization')
        user_id = Users.decode_auth_token(auth_token)
        form_status = request.json.get("form_status",0)
        page_limit = request.json.get("page_limit",10)
        page_num = request.json.get("page_num",1)
        try:
            committed, pending, complete = {"form_status_code":1}, {"form_status_code":2}, {"form_status_code":3}
            if form_permission(user_id) == 1:
                if form_status == 1 or form_status ==0:
                    committed_query = Forms.query.filter_by(submit_dmp_user_id=user_id, approve_result=0)
                    committed["form_count"] = committed_query.count()
                    committed["page_num"] = page_num
                    committed["forms"] = [f.__json__() for f in committed_query.limit(page_limit).offset((page_num-1)*page_limit)]
                if form_status == 3 or form_status ==0:
                    complete_query = Forms.query.filter(Forms.submit_dmp_user_id == user_id,Forms.approve_result != 0)
                    complete["form_count"] = complete_query.count()
                    complete["page_num"] = page_num
                    complete["forms"] = [f.__json__() for f in complete_query.limit(page_limit).offset((page_num-1)*page_limit)]
                return resp_hanlder(result={"committed": committed, "complete": complete})

            elif form_permission(user_id) == 2:
                if form_status == 1 or form_status == 0:
                    committed_query = Forms.query.filter_by(submit_dmp_user_id=user_id, approve_result=0)
                    committed["form_count"] = committed_query.count()
                    committed["page_num"] = page_num
                    committed["forms"] = [f.__json__() for f in committed_query.limit(page_limit).offset((page_num-1)*page_limit)]
                if form_status == 2 or form_status == 0:
                    pending_query = Forms.query.filter(and_(tuple_(Forms.submit_dmp_user_id,).in_(Users.query.with_entities(Users.id).filter_by(leader_dmp_user_id=user_id).all()), Forms.approve_result==0))
                    pending["form_count"] = pending_query.count()
                    pending["page_num"] = page_num
                    pending["forms"] = [f.__json__() for f in pending_query.limit(page_limit).offset((page_num-1)*page_limit)]
                if form_status == 3 or form_status == 0:
                    complete_query = Forms.query.filter(and_(or_(Forms.submit_dmp_user_id == user_id, Forms.approve_dmp_user_id == user_id),Forms.approve_result != 0))
                    complete["form_count"] = complete_query.count()
                    complete["page_num"] = page_num
                    complete["forms"] = [f.__json__() for f in complete_query.limit(page_limit).offset((page_num-1)*page_limit)]
                return resp_hanlder(result={"committed": committed, "pending": pending, "complete": complete})
            elif form_permission(user_id) == 3:
                if form_status == 2 or form_status == 0:
                    pending_query = Forms.query.filter_by(approve_result=0)
                    pending["form_count"] = pending_query.count()
                    pending["page_num"] = page_num
                    pending["forms"] = [f.__json__() for f in pending_query.limit(page_limit).offset((page_num-1)*page_limit)]
                if form_status == 3 or form_status == 0:
                    complete_query = Forms.query.filter(Forms.approve_result != 0)
                    complete["form_count"] = complete_query.count()
                    complete["page_num"] = page_num
                    complete["forms"] = [f.__json__() for f in complete_query.limit(page_limit).offset((page_num-1)*page_limit)]
                return resp_hanlder(result={"pending": pending, "complete": complete})
        except Exception as err:
            return resp_hanlder(code=999, err=err)


def postfunc(meta):
    new_table = meta
    form_id = meta.get("form_id")
    csv_file_path = meta.get("csv_file_path")
    approve_form = Forms.get(form_id)
    try:
        post(
            dmp_data_table_name=new_table.get("dmp_data_table_name"),
            db_table_name=new_table.get("db_table_name"),
            dmp_user_id=new_table.get("dmp_user_id"),
            dmp_database_id=new_table.get("dmp_database_id"),
            dmp_case_id=new_table.get("dmp_case_id"),
            description=new_table.get("description")
        )
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
    except Exception as err:
        approve_form.result = "ASSOCIATION FAILED，ERROR_MSG:%s"%str(err)

    approve_form.finish = True
    approve_form.put()

def dlfunc(meta):
    form_id = meta.get("form_id")
    file_name = meta.get("file_name")
    finally_name = meta.get("finally_name")
    download_path = meta.get("download_path")
    full_name = os.path.join(download_path, finally_name)
    ftp_url = meta.get("ftp_url")
    files = [os.path.join(download_path, f) for f in os.listdir(download_path) if f.startswith(file_name)]
    if len(files) == 1:
        os.rename(files[0], full_name)
    elif len(files) > 1:
        os.rename(files[0], full_name)

        # with open(full_name,"wb") as fp:
        #     for f in files:
        #         data = open(f,"rb")
        #         fp.write(data.read())
        #         data.close()

        for file in files[1:]:
            if os.path.exists(file):
                os.remove(file)
    else:
        pass
    approve_form = Forms.get(form_id)
    approve_form.info_form.filepath = full_name
    approve_form.info_form.ftp_url = ftp_url
    approve_form.info_form.put()
    approve_form.finish = True
    approve_form.put()

def job_finish(meta):
    form_id = meta.get("form_id")
    approve_form = Forms.get(form_id)
    approve_form.finish = True
    approve_form.put()

@form.route("/approve/", methods=["PUT"],
            defaults={"desc": {"interface_name": "表单审批", "is_permission": True, "permission_belong": 2}})
def approve(desc):
    if request.method == "PUT":
        try:
            # 获取请求参数
            approve_form_info = request.json
            auth_token = request.headers.get('Authorization')
            approve_user_id = Users.decode_auth_token(auth_token)
            form_type = approve_form_info.get("dmp_form_type", None)
            form_id = approve_form_info.get("dmp_form_id", None)
            approve_result = approve_form_info.get("approve_result", None)
            answer = approve_form_info.get("answer", None)
            # 保存表单审批信息
            approve_form = Forms.get(form_id)
            approve_form.approve_dmp_user_id = approve_user_id
            approve_form.approve_result = approve_result
            approve_form.approve_on = datetime.datetime.now()
            approve_form.answer = answer
            # approve_form.put()
            # 执行审批动作
            if form_type == 1:
                # 从数据库添加数据表单
                try:
                    if approve_result == 1:
                        post(
                            dmp_data_table_name=approve_form.info_form.dmp_data_table_name,
                            db_table_name=approve_form.info_form.db_table_name,
                            dmp_user_id=approve_form.submit_dmp_user_id,
                            dmp_database_id=approve_form.info_form.dmp_database_id,
                            dmp_case_id=approve_form.info_form.dmp_case_id,
                            description=approve_form.description
                        )
                    approve_form.result = "SUCCEED！"
                except Exception as err:
                    approve_form.result = "ASSOCIATION FAILED，ERROR_MSG:%s"%str(err)
                approve_form.finish = True

            elif form_type == 2:
                # 文件上传添加数据表单
                upload_path = current_app.config.get("UPLOADED_PATH")
                file_path = os.path.join(upload_path, approve_form.info_form.filepath)
                file_type = approve_form.info_form.filetype
                column_line = approve_form.info_form.column_line
                column = approve_form.info_form.column.split(",") if type(approve_form.info_form.column) == str else []
                destination_dmp_database_id = approve_form.info_form.destination_dmp_database_id
                destination_db_table_name = approve_form.info_form.destination_db_table_name
                dmp_data_table_name = approve_form.info_form.dmp_data_table_name
                method = approve_form.info_form.method
                description = approve_form.description
                submit_dmp_user_id = approve_form.submit_dmp_user_id
                dmp_case_id = approve_form.dmp_case_id

                destination_database = Database.get(destination_dmp_database_id)
                destination_database_type = destination_database.db_type
                destination_db_host = destination_database.db_host
                destination_db_port = destination_database.db_port
                destination_db_username = destination_database.db_username
                destination_db_passwd = destination_database.db_passwd
                destination_db_name = destination_database.db_name
                try:
                    reader = []
                    text_column = []
                    csv_filepath = os.path.join(current_app.config.get("UPLOADED_PATH"), file_path)
                    if file_type == 1 or file_type == 3:
                        # csv、excel
                        dt = pd.read_csv(csv_filepath, header=column_line)
                        csv_column = list(dt.columns)
                        text_column = column if column and len(column) == len(csv_column) else csv_column
                        csv_column_d = [{"index": i, "type": "string"} for i, cc in enumerate(text_column)]
                        reader = textfile_reader(
                            filepath=csv_filepath,
                            column=csv_column_d
                        )
                    elif file_type == 2:
                        # json
                        dt = pd.read_csv(csv_filepath, header=0)
                        csv_column = list(dt.columns)
                        text_column = column if column and len(column) == len(csv_column) else csv_column
                        csv_column_d = [{"index": i, "type": "string"} for i, cc in enumerate(text_column)]
                        reader = textfile_reader(
                            filepath=csv_filepath,
                            column=csv_column_d
                        )
                        pass
                    writer = []
                    if destination_database_type == 1:
                        # hive_writer
                        hive_columns = [{"name": col, "type": "string"} for col in text_column]
                        hive_path = "/user/hive/warehouse/%s.db/%s" % (destination_db_name, destination_db_table_name)
                        hive_conn = auto_connect(destination_dmp_database_id)
                        create_table_sql = create_table_query_handler(table_name=destination_db_table_name,
                                                                      fields=text_column,
                                                                      uniform_type="string",
                                                                      id_primary_key=False,
                                                                      semicolon=False,
                                                                      fieldDelimiter=",")

                        # current_app.logger.info(create_table_sql)
                        if method == 1:
                            hive_conn.execsql(create_table_sql)
                        elif method == 3:
                            del_table_sql = "drop table {table_name}"
                            hive_conn.execsql(del_table_sql.format(table_name=destination_db_table_name))
                            hive_conn.execsql(create_table_sql)
                        else:
                            pass
                        writer = hive_writer(host=destination_db_host,
                                             port=8020,
                                             path=hive_path,
                                             filename=destination_db_table_name,
                                             column=hive_columns,
                                             fieldDelimiter=",",
                                             )

                    elif destination_database_type == 2:
                        # mysql_writer
                        create_table_sql = create_table_query_handler(table_name=destination_db_table_name,
                                                                      fields=text_column,
                                                                      uniform_type="text",
                                                                      id_primary_key=True,
                                                                      semicolon=True,
                                                                      fieldDelimiter=None)
                        current_app.logger.info(create_table_sql)
                        mysql_conn = auto_connect(destination_dmp_database_id)
                        del_table_sql = "drop table {table_name};"
                        if method == 1:
                            mysql_conn.execsql(sql=create_table_sql)
                        elif method == 2:
                            pass
                        elif method == 3:
                            mysql_conn.execsql(del_table_sql.format(table_name=destination_db_table_name))
                            mysql_conn.execsql(create_table_sql)
                        column = text_column
                        writer = mysql_writer(model=1,
                                              username=destination_db_username,
                                              password=destination_db_passwd,
                                              column=column,
                                              host=destination_db_host,
                                              port=destination_db_port,
                                              db=destination_db_name,
                                              table=destination_db_table_name,
                                              )
                    elif destination_database_type == 3:
                        # mongo_writer
                        mongo_conn = auto_connect(destination_dmp_database_id)
                        if method == 3:
                            mongo_conn.del_table(table_name=destination_db_table_name)
                        column = [{"name": col, "type": "string"} for col in text_column]
                        writer = mongodb_writer(host=destination_db_host,
                                                port=destination_db_port,
                                                username=destination_db_username,
                                                password=destination_db_passwd,
                                                db_name=destination_db_name,
                                                collection_name=destination_db_table_name,
                                                column=column,
                                                )
                    meta = {
                        "form_id":approve_form.id,
                        "csv_file_path":csv_filepath,
                        "dmp_data_table_name": dmp_data_table_name,
                        "db_table_name": destination_db_table_name,
                        "dmp_user_id": submit_dmp_user_id,
                        "dmp_database_id": destination_dmp_database_id,
                        "dmp_case_id": dmp_case_id,
                        "description": description,
                    }
                    job_hanlder.delay(reader=reader, writer=writer, func=postfunc, meta=meta)
                    approve_form.result = "SUCCEED!"
                except Exception as err:
                    approve_form.result = "CREATE UPLOAD JOB FAILED，ERROR MESSAGE：%s"%str(err)




            elif form_type == 3:
                # 数据迁移表单

                if approve_result == 1:
                    origin_data_table = DataTable.get(approve_form.info_form.origin_dmp_table_id)
                    origin_database = Database.get(origin_data_table.dmp_database_id)
                    origin_database_type = origin_database.db_type
                    origin_db_host = origin_database.db_host
                    origin_db_port = origin_database.db_port
                    origin_db_username = origin_database.db_username
                    origin_db_passwd = origin_database.db_passwd
                    origin_db_name = origin_database.db_name
                    origin_db_table_name = origin_data_table.db_table_name

                    destination_database = Database.get(approve_form.info_form.destination_dmp_database_id)
                    destination_database_type = destination_database.db_type
                    destination_db_host = destination_database.db_host
                    destination_db_port = destination_database.db_port
                    destination_db_username = destination_database.db_username
                    destination_db_passwd = destination_database.db_passwd
                    destination_db_name = destination_database.db_name
                    destination_db_table_name = approve_form.info_form.new_table_name

                    try:
                        base_column = auto_connect(origin_data_table.dmp_database_id).columns(
                            origin_data_table.db_table_name)
                        # current_app.logger.info(base_column)
                        reader = []
                        if origin_database_type == 1:
                            # hive_reader
                            reader = hive_reader(host=origin_db_host,
                                                 port=8020,
                                                 path="/user/hive/warehouse/%s.db/%s" % (
                                                     origin_db_name, origin_db_table_name),
                                                 fileType="text",
                                                 column=["*"],
                                                 fieldDelimiter=',',
                                                 encoding="utf-8"
                                                 )
                        elif origin_database_type == 2:
                            # mysql_reader
                            column = [col.get("dmp_data_table_column_name") for col in base_column]
                            reader = mysql_reader(username=origin_db_username,
                                                  password=origin_db_passwd,
                                                  column=column,
                                                  host=origin_db_host,
                                                  port=origin_db_port,
                                                  db=origin_db_name,
                                                  table=origin_db_table_name,
                                                  where=None,
                                                  )

                        elif origin_database_type == 3:
                            # mongodb
                            column = [{"index": i + 1, "name": col.get("dmp_data_table_column_name"),
                                       "type": col.get("dmp_data_table_column_type")} for i, col in enumerate(base_column)]
                            reader = mongodb_reader(host=origin_db_host,
                                                    port=origin_db_port,
                                                    db_name=origin_db_name,
                                                    collection_name=origin_db_table_name,
                                                    column=column,
                                                    username=origin_db_username,
                                                    password=origin_db_passwd
                                                    )
                            pass
                        writer = []
                        if destination_database_type == 1:
                            # hive_writer
                            hive_col = [col.get("dmp_data_table_column_name") for col in base_column]
                            hive_columns = [{"name": col, "type": "string"} for col in hive_col]
                            hive_path = "/user/hive/warehouse/%s.db/%s" % (destination_db_name, destination_db_table_name)
                            hive_conn = auto_connect(approve_form.destination_dmp_database_id)
                            create_table_sql = create_table_query_handler(table_name=destination_db_table_name,
                                                                          fields=hive_col,
                                                                          uniform_type="string",
                                                                          id_primary_key=False,
                                                                          semicolon=False,
                                                                          fieldDelimiter=",")

                            hive_conn.execsql(create_table_sql)

                            writer = hive_writer(host=destination_db_host,
                                                 port=8020,
                                                 path=hive_path,
                                                 filename=destination_db_table_name,
                                                 column=hive_columns,
                                                 fieldDelimiter=",",
                                                 )
                        elif destination_database_type == 2:
                            # mysql_writer
                            column = [col.get("dmp_data_table_column_name") for col in base_column]
                            create_table_sql = create_table_query_handler(table_name=destination_db_table_name,
                                                                          fields=column,
                                                                          uniform_type="text",
                                                                          id_primary_key=True,
                                                                          semicolon=True,
                                                                          fieldDelimiter=None)
                            mysql_conn = auto_connect(approve_form.destination_dmp_database_id)
                            mysql_conn.execsql(sql=create_table_sql)
                            preSQL = []
                            writer = mysql_writer(model=1,
                                                  username=destination_db_username,
                                                  password=destination_db_passwd,
                                                  column=column,
                                                  host=destination_db_host,
                                                  port=destination_db_port,
                                                  db=destination_db_name,
                                                  table=destination_db_table_name,
                                                  )
                        elif destination_database_type == 3:
                            # mongo_writer
                            column = [{"name": col.get("dmp_data_table_column_name"), "type": "string"} for col in
                                      base_column]
                            writer = mongodb_writer(host=destination_db_host,
                                                    port=destination_db_port,
                                                    username=destination_db_username if destination_db_username else None,
                                                    password=destination_db_passwd if destination_db_passwd else None,
                                                    db_name=destination_db_name,
                                                    collection_name=destination_db_table_name,
                                                    column=column,
                                                    )

                        job_hanlder.delay(reader=reader, writer=writer)
                    except Exception as err:
                        approve_form.result = "CREATE MIGRATE JOB FAILED，ERROR MESSAGE：%s"%str(err)

            elif form_type == 4:
                # 数据导出表单
                if approve_result == 1:
                    origin_data_table = DataTable.get(approve_form.info_form.dmp_data_table_id)
                    origin_database = Database.get(origin_data_table .dmp_database_id)
                    origin_database_type = origin_database.db_type
                    origin_db_host = origin_database.db_host
                    origin_db_port = origin_database.db_port
                    origin_db_username = origin_database.db_username
                    origin_db_passwd = origin_database.db_passwd
                    origin_db_name = origin_database.db_name
                    origin_db_table_name = origin_data_table.db_table_name
                    try:
                        base_column = auto_connect(origin_data_table.dmp_database_id).columns(
                            origin_data_table.db_table_name)

                        reader = []
                        if origin_database_type == 1:
                            # hive_reader
                            reader = hive_reader(host=origin_db_host,
                                                 port=8020,
                                                 path="/user/hive/warehouse/%s.db/%s" % (
                                                     origin_db_name, origin_db_table_name),
                                                 fileType="text",
                                                 column=["*"],
                                                 fieldDelimiter=',',
                                                 encoding="utf-8"
                                                 )
                        elif origin_database_type == 2:
                            # mysql_reader
                            column = [col.get("dmp_data_table_column_name") for col in base_column]
                            reader = mysql_reader(username=origin_db_username,
                                                  password=origin_db_passwd,
                                                  column=column,
                                                  host=origin_db_host,
                                                  port=origin_db_port,
                                                  db=origin_db_name,
                                                  table=origin_db_table_name,
                                                  where=None,
                                                  )

                        elif origin_database_type == 3:
                            # mongodb
                            column = [{"index": i + 1, "name": col.get("dmp_data_table_column_name"),
                                       "type": col.get("dmp_data_table_column_type")} for i, col in enumerate(base_column)]
                            reader = mongodb_reader(host=origin_db_host,
                                                    port=origin_db_port,
                                                    db_name=origin_db_name,
                                                    collection_name=origin_db_table_name,
                                                    column=column,
                                                    username=origin_db_username,
                                                    password=origin_db_passwd
                                                    )
                            pass
                        writer = []
                        download_path = os.path.join(current_app.config.get("DOWNLOAD_PATH"),
                                                     approve_form.submit_users.dmp_username)
                        file_name = origin_db_table_name + uuid_str() + ".csv"
                        finally_name = origin_db_table_name + "-" + uuid_str() + ".csv"
                        headers = [col.get("dmp_data_table_column_name") for col in base_column]
                        writer = textfile_writer(filepath=download_path, filename=file_name, header=headers)

                        job_hanlder.delay(reader=reader, writer=writer)
                        ip = socket.gethostbyname(socket.gethostname())
                        ftp_url = "ftp://%s:21/%s" % (
                            str(ip), str(os.path.join(approve_form.submit_users.dmp_username, finally_name)))

                        meta = {
                            "form_id": approve_form.id,
                            "file_name": file_name,
                            "finally_name": finally_name,
                            "download_path": download_path,
                            "ftp_url": ftp_url,
                        }
                        job_hanlder.delay(reader=reader, writer=writer, func=dlfunc, meta=meta)
                    except Exception as err:
                        approve_form.result = "CREATE DOWNLOAD JOB FAILED，ERROR MESSAGE：%s"%str(err)

            approve_form.put()
            return resp_hanlder(result="OK!")
        except Exception as err:
            raise err
            return resp_hanlder(code=999, err=err, msg=str(err))
