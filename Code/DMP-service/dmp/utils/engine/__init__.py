#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD


from .hive_engine import HiveEngone
from .mongo_engine import MongodbEngine
from .mysql_engine import MysqlEngine

engines = {
    1: HiveEngone,
    3: MongodbEngine,
    2: MysqlEngine,
}


def auto_connect(db_id):
    try:
        from dmp.models import Database
        db = Database.get(db_id)
        Engine = engines.get(db.db_type)
        conn = Engine(host=db.db_host, port=db.db_port, user=db.db_username, passwd=db.db_passwd, db=db.db_name)
        return conn
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
    columns = ",".join(["%s %s" % (col, uniform_type) for col in fields if id_primary_key!=True & col != "id"])
    p1 = id_pri if id_primary_key else ""
    p2 = Delimiter.format(fieldDelimiter=fieldDelimiter) if fieldDelimiter else ""
    p3 = ";" if semicolon else ""
    sql = create.format(table_name=table_name) + p1 + col.format(
        columns=columns) + p2 + p3

    return sql
