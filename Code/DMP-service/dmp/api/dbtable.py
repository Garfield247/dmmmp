#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD


from flask import Blueprint, request, current_app
from dmp.models import DataTable, Users, Database,DataTableColumn
from dmp.utils import resp_hanlder
from dmp.utils.engine import MongodbEngine,MysqlEngine
from dmp.utils.engine import auto_connect

dbtable = Blueprint("dbtable", __name__)


@dbtable.route("/info/", methods=["GET"], defaults={"desc": "获取数据表信息"})
def info(desc):
    if request.method == "GET":
        try:
            dmp_data_table_id = request.json.get("dmp_data_table_id")
            dmp_case_id = request.json.get("dmp_case_id")
            if dmp_case_id and not dmp_data_table_id:
                dbtables = [dtb.__json__() for dtb in DataTable.query.filter_by(dmp_case_id=dmp_case_id).all()]
                current_app.logger.info(dbtables)
                return resp_hanlder(result=dbtables)
            elif dmp_data_table_id and not dmp_case_id:
                db_table = DataTable.get(dmp_data_table_id).__json__()
                current_app.logger.info(db_table)
                return resp_hanlder(result=db_table)
        except Exception as err:
            return resp_hanlder(err=err)


@dbtable.route("/all/",methods=["GET"],defaults={"desc":"获取所有数据表信息"})
def all(desc):
    if request.method == "GET":
        try:
            dbtables = []
            for dtb in DataTable.query.all():
                dtb_d = dtb.__json__()
                dtb_d["case_name"] = dtb.case.dmp_case_name
                dtb_d["database_name"] = dtb.database.dmp_database_name
                dtb_d["user_name"] = dtb.users.dmp_username
                dbtables.append(dtb_d)
                current_app.logger.info(dbtables)
            return resp_hanlder(result=dbtables)
        except Exception as err:
            return resp_hanlder(err=err)

def post(dmp_data_table_name,
         db_table_name,
         description,
         dmp_user_id,
         dmp_database_id,
         dmp_case_id):
    """添加数据表"""
    new_db_table = DataTable(
        dmp_data_table_name=dmp_data_table_name,
        db_table_name=db_table_name,
        description=description,
        dmp_user_id=dmp_user_id,
        dmp_database_id=dmp_database_id,
        dmp_case_id=dmp_case_id)
    new_db_table.save()
    print("new data table saved")
    new_db_table.data_count()
    return new_db_table.__json__()


@dbtable.route("/put/",methods=["PUT"],defaults={"desc":"修改数据表信息"})
def put(desc):
    if request.method =="PUT":
        auth_token = request.headers.get('Authorization')
        current_user_id = Users.decode_auth_token(auth_token)
        dbt_info = request.json
        dbt_id = dbt_info.get("dmp_data_table_id")
        dbt_name = dbt_info.get("dmp_data_table_name")
        description = dbt_info.get("description")
        dbt = DataTable.get(dbt_id)
        if dbt:
            dmp_user_id = dbt.dmp_user_id
            if current_user_id ==1 or current_user_id == dmp_user_id or Users.get(dmp_user_id).leader_dmp_user_id == current_user_id:
                if dbt_name:
                    dbt.dmp_data_table_name = dbt_name
                if description:
                    dbt.description = description
                dbt.put()
                return  resp_hanlder(result="OK!")
            else:
                return  resp_hanlder(code=301)
        else:
            return  resp_hanlder(code=404)


@dbtable.route("/column/", methods=["GET"], defaults={"desc": "获取数据表的列信息"})
def column(desc):
    if request.method == "GET":
        try:
            dmp_data_table_id = request.json.get("dmp_data_table_id")
            data_table_info = DataTable.get(dmp_data_table_id)
            current_app.logger.info(data_table_info.__json__())
            db_table_name = data_table_info.db_table_name
            database_info = Database.get(data_table_info.dmp_database_id)
            current_app.logger.info(database_info.__json__())
            db_type = database_info.db_type
            db_host = database_info.db_host
            db_port = database_info.db_port
            db_name = database_info.db_name
            db_username = database_info.db_username
            db_passwd = database_info.db_passwd

            colums4sdb = DataTableColumn.query.filter_by(dmp_data_table_id=dmp_data_table_id)
            column4sdb_array = []
            current_app.logger.info(colums4sdb.count())
            if colums4sdb.count()>0:
                column4sdb_array = [col.__json__() for col in colums4sdb.all()]
            columns4db = []
            if db_type == 1:
                # hive
                pass
            elif db_type == 2:
                # mysql
                db = MysqlEngine(host=db_host,port=db_port,user=db_username,passwd=db_passwd,db=db_name)
                columns4db = db.columns(db_table_name)
            elif db_type == 3:
                # mongo
                db = MongodbEngine(host=db_host,port=db_port,user=db_username,passwd=db_passwd,db=db_name)
                columns4db = db.columns(db_table_name)
            # dmp_data_table_column_name
            current_app.logger.info(column4sdb_array)
            columns = []
            for i in columns4db:
                mark=True
                for j in column4sdb_array:
                    if j.get("dmp_data_table_column_name") == i.get("dmp_data_table_column_name"):
                        columns.append(j)
                        mark = False
                if mark:
                    columns.append(i)
            current_app.logger.info(columns)
            return resp_hanlder(result=columns)
        except Exception as err:
            current_app.logger.error(err)
            return  resp_hanlder(code=999,err=err)


@dbtable.route("/columnsetting/", methods=["POST"], defaults={"desc": "数据表的数据列设置"})
def columnsetting(desc):
    if request.method == "POST":
        columns_info = request.json
        dmp_data_table_id  = columns_info.get("dmp_data_table_id")
        columns = columns_info.get("columns")
        for col in columns:
            column_id = col.get("id")
            dmp_data_table_column_name = col.get("dmp_data_table_column_name")
            dmp_data_table_column_type = col.get("dmp_data_table_column_type")
            groupby = col.get("groupby")
            wherein = col.get("wherein")
            isdate = col.get("isdate")
            description = col.get("description")

            if column_id:
                col_ = DataTableColumn.get(column_id)
                col_.dmp_data_table_column_name = dmp_data_table_column_name
                col_.dmp_data_table_column_type = dmp_data_table_column_type
                col_.groupby = groupby
                col_.wherein = wherein
                col_.isdate = isdate
                col_.description = description
                col_.dmp_data_table_id = dmp_data_table_id
                col_.put()
            else:
                col_ = DataTableColumn(
                    dmp_data_table_column_name = dmp_data_table_column_name,
                    dmp_data_table_column_type = dmp_data_table_column_type,
                    groupby = groupby,
                    wherein = wherein,
                    isdate = isdate,
                    description = description,
                    dmp_data_table_id=dmp_data_table_id
                )
                col_.save()

        return resp_hanlder(result="OK!")


@dbtable.route("/retrieve/",methods=["GET"],defaults={"desc":"数据查询"})
def retrieve(desc):
    if request.method == "GET":
        retrieve_info = request.json
        dmp_data_table_id = retrieve_info.get("dmp_data_table_id")
        dmp_data_table = DataTable.get(dmp_data_table_id)
        database_id = dmp_data_table.dmp_database_id
        db_table_name = dmp_data_table.db_table_name
        conn = auto_connect(db_id=database_id)
        data = conn.retrieve(db_table_name)
        current_app.logger.info(data)
        return  resp_hanlder(result=data)


@dbtable.route("/del/", methods=["DELETE"], defaults={"desc": "删除数据表"})
def dbtdel(desc):
    if request.method == "DELETE":
        try:
            auth_token = request.headers.get('Authorization')
            current_user_id = Users.decode_auth_token(auth_token)
            del_data_table_id = request.json.get("dmp_data_table_id")
            if del_data_table_id:
                del_data_table = DataTable.get(del_data_table_id)
                if del_data_table:
                    is_user = Users.get(DataTable.get(del_data_table_id).dmp_user_id).id == current_user_id
                    is_user_leader = Users.get(DataTable.get(del_data_table_id).dmp_user_id).leader_dmp_user_id == current_user_id
                    is_admin = Users.get(current_user_id).dmp_group_id == 1
                    if is_user or is_user_leader or is_admin:
                        del_data_table.delete()
                        current_app.logger.info("del db table complete!")
                        return resp_hanlder(result="OK")
                    else:
                        return resp_hanlder(code=501)
                else:
                    return resp_hanlder(code=404)
            else:
                return resp_hanlder(code=101)
        except Exception as err:
            return resp_hanlder(err=err)
