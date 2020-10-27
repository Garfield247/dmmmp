#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD

from flask import current_app
from .hive_engine import HiveEngine
from .mongo_engine import MongodbEngine
from .mysql_engine import MysqlEngine
from .kylin_engine import KylinEngin

engines = {
    1: HiveEngine,
    3: MongodbEngine,
    2: MysqlEngine,
    4: KylinEngin,
}


def auto_connect(db_id=None, table_id=None):
    try:
        from dmp.models import Database, DataTable
        if table_id != None  and db_id==None:
            if DataTable.exist_item_by_id(table_id):
                table = DataTable.get(table_id)
                db_id = table.dmp_database_id
                if Database.exist_item_by_id(db_id):
                    db = Database.get(db_id)
                    db_type = 4 if db.db_type == 1 and table.is_kylin else db.db_type
                    Engine = engines.get(db_type)
                    if db_type == 4:
                        conn = Engine(
                            host = current_app.config.get("KYLIN_HOST"),
                            port = current_app.config.get("KYLIN_PORT"),
                            user = current_app.config.get("KYLIN_USER"),
                            passwd= current_app.config.get("KYLIN_PASSWD"),
                            db = current_app.config.get("KYLIN_PROJECT")
                            )

                    else:
                        conn = Engine(
                            host=db.db_host,
                            port=db.db_port,
                            user=db.db_username,
                            passwd=db.db_passwd,
                            db=db.db_name
                            )
                return conn
            else:
                print("数据表不存在")
                raise Exception("数据表不存在")

        elif db_id != None:
            if Database.exist_item_by_id(db_id):

                db = Database.get(db_id)
                Engine = engines.get(db.db_type)
                conn = Engine(host=db.db_host, port=db.db_port,
                              user=db.db_username, passwd=db.db_passwd, db=db.db_name)
                return conn
            else:
                print("数据库不存在")
                raise Exception("数据库不存在")
        else:
            raise Exception("缺少必要参数")
    except Exception as e:
        raise e


def create_table_query_handler(table_name, fields, uniform_type, id_primary_key=True, semicolon=True,
                               fieldDelimiter=None):
    create = "create table {table_name}("
    id_pri = "id int  auto_increment primary key,"
    col = "{columns})"
    Delimiter = "row format delimited fields terminated by '{fieldDelimiter}'"
    # if id_primary_key and "id" in fields:
    #     fields.remove("id")
    ccc = ["%s %s" % (col, uniform_type)if id_primary_key != True and col != "id" else None for col in fields ]
    if None in ccc:
        ccc.remove(None)
    columns = ",".join(ccc)
    p1 = id_pri if id_primary_key else ""
    p2 = Delimiter.format(
        fieldDelimiter=fieldDelimiter) if fieldDelimiter else ""
    p3 = ";" if semicolon else ""
    sql = create.format(table_name=table_name) + p1 + col.format(
        columns=columns) + p2 + p3

    return sql
