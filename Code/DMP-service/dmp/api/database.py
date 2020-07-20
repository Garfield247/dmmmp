#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import Blueprint, request, current_app
from dmp.models import Database, Users, DataTable
from dmp.utils import resp_hanlder
from dmp.utils.engine import auto_connect

database = Blueprint("database", __name__)


@database.route("/info/", methods=["GET"], defaults={"desc": {"interface_name": "数据库信息","is_permission": True,"permission_belong": 0}})
def info(desc):
    if request.method == "GET":
        auth_token = request.headers.get('Authorization')
        current_user_id = Users.decode_auth_token(auth_token)
        try:
            database_id = request.json.get("dmp_database_id") if request.json else None
            if database_id:
                data = Database.query.get(database_id).__json__()
            else:
                data = []
                if Users.get(current_user_id).dmp_group_id == 1:
                    data = [d.__json__() for d in Database.query.all()]
                else:
                    user_ids = [u.id for u in Users.query.filter_by(leader_dmp_user_id=current_user_id).all()]
                    user_ids.append(current_user_id)
                    # current_app.logger.info(user_ids)
                    data = [d.__json__() for d in
                            Database.query.filter(Database.dmp_user_id.in_(user_ids) | Database.ispublic == True).all()]
                # current_app.logger.info(data)
            return resp_hanlder(result=data)
        except Exception as err:
            return resp_hanlder(code=999, err=err)


@database.route("/del/", methods=["DELETE"], defaults={"desc": {"interface_name": "删除数据库连接信息","is_permission": True,"permission_belong": 0}})
def dbdel(desc):
    if request.method == "DELETE":
        try:
            auth_token = request.headers.get('Authorization')
            current_user_id = Users.decode_auth_token(auth_token)
            del_database_id = request.json.get("dmp_database_id")
            if del_database_id:
                del_database = Database.get(del_database_id)
                if del_database:
                    is_user = Database.get(del_database_id).dmp_user_id == current_user_id
                    is_user_leader = Users.get(Database.get(del_database_id).dmp_user_id).leader_dmp_user_id == current_user_id
                    is_admin = Users.get(current_user_id).dmp_group_id == 1
                    if is_user or is_user_leader or is_admin:
                        try:
                            del_database.delete()
                            current_app.logger.info("del db complete!")
                            return resp_hanlder(result="OK")
                        except Exception as err:
                            msg = "The database already has data association and cannot be deleted"
                            return resp_hanlder(code=502,msg=msg)
                    else:
                        return resp_hanlder(code=301)
                else:
                    return resp_hanlder(code=404)
            else:
                return resp_hanlder(code=101)
        except Exception as err:
            return resp_hanlder(code=999,err=err,msg=str(err))


@database.route("/connect/", methods=["POST"], defaults={"desc": {"interface_name": "测试数据库连接","is_permission": False,"permission_belong": None}})
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
                # from pyhive import hive
                # conn = hive.Connection(host=db_host, port=db_port, username=db_user, password=db_password,
                #                        database=db_name)
                # current_app.logger.info(conn.client)
                from dmp.utils.engine import HiveEngone
                hive_conn = HiveEngone(host=db_host, port=db_port, user=db_user, passwd=db_password, db=db_name)
                hive_conn.close_conn()
                res = {"connect": "ok!"}
            except Exception as err:
                return resp_hanlder(code=303, msg=str(err))
        elif int(db_type) == 2:
            try:
                import pymysql
                current_app.logger.info(db_host)
                conn = pymysql.connect(port=db_port, host=db_host, user=db_user, passwd=db_password, db=db_name,
                                       charset='utf8mb4')
                current_app.logger.info(conn.server_version)
                conn.close()
                res = {"connect": "ok!"}
            except Exception as err:
                return resp_hanlder(code=303, msg=str(err))
        elif int(db_type) == 3:
            try:
                from pymongo import MongoClient
                conn = MongoClient(host=db_host, port=db_port, username=db_user, password=db_password)
                current_app.logger.info(conn.server_info())
                conn.close()
                res = {"connect": "ok!"}

            except Exception as err:
                return resp_hanlder(code=303, msg=str(err))
        return resp_hanlder(result=res)


@database.route("/table_list/", methods=["GET"], defaults={"desc": {"interface_name": "获取数据库的数据表","is_permission": True,"permission_belong": 0}})
def table_list(desc):
    if request.method == "GET":
        db_id = request.json.get("dmp_database_id")
        conn = auto_connect(db_id=db_id)
        res = conn.tables_list
        current_app.logger.info(res)
        return resp_hanlder(result=res)


@database.route("/post/", methods=["POST", "PUT"], defaults={"desc": {"interface_name": "添加/修改数据库信息","is_permission": True,"permission_belong": 0}})
def post(desc):
    db_info = request.json
    auth_token = request.headers.get('Authorization')
    current_user_id = Users.decode_auth_token(auth_token)
    if request.method == "POST":
        try:
            new_db = Database(
                dmp_database_name=db_info.get("dmp_database_name"),
                db_type=db_info.get("db_type"),
                db_host=db_info.get("db_host"),
                db_port=db_info.get("db_port"),
                db_username=db_info.get("db_username"),
                db_passwd=db_info.get("db_passwd"),
                db_name=db_info.get("db_name"),
                ispublic=db_info.get("ispublic"),
                description=db_info.get("description"),
                dmp_user_id=current_user_id,
            )
            new_db.save()
            current_app.logger.info("add new database")
            return resp_hanlder(result={"add_database": "complete!"})
        except Exception as err:
            return resp_hanlder(code=200, err=err)
    elif request.method == "PUT":
        try:
            if db_info.get("dmp_database_id"):
                modify_db = Database.get(db_info.get("dmp_database_id"))
                if "dmp_database_name" in db_info.keys():
                    modify_db.dmp_database_name = db_info.get("dmp_database_name")
                if "db_type" in db_info.keys():
                    modify_db.db_type = db_info.get("db_type")
                if "db_host" in db_info.keys():
                    modify_db.db_host = db_info.get("db_host")
                if "db_port" in db_info.keys():
                    modify_db.db_port = db_info.get("db_port")
                if "db_username" in db_info.keys():
                    modify_db.db_username = db_info.get("db_username")
                if "db_passwd" in db_info.keys():
                    modify_db.db_passwd = db_info.get("db_passwd")
                if "db_name" in db_info.keys():
                    modify_db.db_name = db_info.get("db_name")
                if "ispublic" in db_info.keys():
                    modify_db.ispublic = True if db_info.get("ispublic") else False
                if "description" in db_info.keys():
                    modify_db.description = db_info.get("description")
                modify_db.put()
                current_app.logger.info("database info modify complete!")
                return resp_hanlder(result={"modify": "ok!"})
            else:
                return resp_hanlder(code=101)
        except Exception as err:
            return resp_hanlder(code=999, err=err)
