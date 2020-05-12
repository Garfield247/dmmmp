#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import Blueprint, jsonify, request, current_app
from dmp.models import Database,Users,DataTable
from dmp.utils import resp_hanlder

database = Blueprint("database",__name__)

@database.route("/info/",methods=["GET"],defaults={"desc":"数据库信息"})
def info(desc):
    if request.method == "GET":
        try:
            database_id = request.json.get("dmp_database_id") if request.json else None
            if database_id:
                data = Database.query.get(database_id).__json__()
            else:
                data = [d.__json__() for d in  Database.query.all()]
            return resp_hanlder(result=data)
        except Exception as err:
            return resp_hanlder(code=999,err=err)


@database.route("/del/",methods=["DELETE"],defaults={"desc":"删除数据库连接信息"})
def dbdel(desc):
    if request.method == "DELETE":
        try:
            current_user_id = 3
            # current_user_id = get_current_user().id
            del_database_id = request.json.get("dmp_database_id")
            if del_database_id:
                del_database = Database.get(del_database_id)
                if del_database:
                    is_user = Users.get(Database.get(del_database_id).dmp_user_id).id == current_user_id
                    is_user_leader = Users.get(Database.get(del_database_id).dmp_user_id).leader_dmp_user_id == current_user_id
                    is_admin = Users.get(current_user_id).dmp_group_id == 1
                    if is_user or is_user_leader or is_admin:
                        # current_app.logger.info(DataTable.query.filter_by(dmp_database_id=current_user_id).count())
                        if DataTable.query.filter_by(dmp_database_id=current_user_id).count() == 0:
                            del_database.delete()
                            current_app.logger.info("del db complete!")
                            return resp_hanlder(result="OK")
                        else:
                            return resp_hanlder(code=401)
                    else:
                        return resp_hanlder(code=301)
                else:
                    return resp_hanlder(code=404)
            else:
                return resp_hanlder(code=101)
        except Exception as err:
            return resp_hanlder(err=err)


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
                return resp_hanlder(code=303,err=err)
        elif int(db_type) == 2:
            try:
                from pymongo import MongoClient
                conn = MongoClient(host=db_host,port=db_port,username=db_user,password=db_password)
                current_app.logger.info(conn.server_info())
                res = {"connect":"ok!"}
            except Exception as err:
                return resp_hanlder(code=303,err=err)
        elif int(db_type) == 3:
            try:
                from pyhive import hive
                conn = hive.Connection(host=db_host,port=db_port,username=db_user,password=db_password,database=db_name)
                current_app.logger.info(conn.__dict__)
            except Exception as err:
                return resp_hanlder(code=303,err=err)
        return resp_hanlder(result=res)

@database.route("/post/",methods=["POST","PUT"],defaults={"desc":"添加/修改数据库信息"})
def post(desc):
    db_info = request.json
    current_user_id = 3
    # current_user_id = get_current_user().id
    if request.method == "POST":
        try:
            new_db = Database(
                dmp_database_name = db_info.get("dmp_database_name"),
                db_type = db_info.get("db_type"),
                db_host = db_info.get("db_host"),
                db_port = db_info.get("db_port"),
                db_username = db_info.get("db_username"),
                db_passwd = db_info.get("db_passwd"),
                db_name= db_info.get("db_name"),
                description = db_info.get("description"),
                dmp_user_id = current_user_id,
            )
            new_db.save()
            current_app.logger.info("add new database")
            return resp_hanlder(result={"add_database":"complete!"})
        except Exception as err:
            return resp_hanlder(code=200,err=err)
    elif request.method == "PUT":
        if db_info.get("dmp_database_id"):
            modify_db = Database.get(db_info.get("dmp_database_id"))
            if db_info.get("dmp_database_name"):
                modify_db.dmp_database_name = db_info.get("dmp_database_name")
            if db_info.get("db_type"):
                modify_db.db_type = db_info.get("db_type")
            if db_info.get("db_host"):
                modify_db.db_host = db_info.get("db_host")
            if db_info.get("db_port"):
                modify_db.db_port = db_info.get("db_port")
            if db_info.get("db_username"):
                modify_db.db_username = db_info.get("db_username")
            if db_info.get("db_passwd"):
                modify_db.db_passwd = db_info.get("db_passwd")
            if db_info.get("db_name"):
                modify_db.db_name = db_info.get("db_name")
            if db_info.get("description"):
                modify_db.description = db_info.get("description")
            modify_db.put()
            current_app.logger.info("database info modify complete!")
            return resp_hanlder(result={"modify":"ok!"})
        else:
            return resp_hanlder(code=101)
