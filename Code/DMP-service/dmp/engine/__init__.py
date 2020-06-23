#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD


from .hive_engine import HiveEngone
from .mongo_engine import MongodbEngine
from .mysql_engine import MysqlEngine



engines = {
    1:HiveEngone,
    3:MongodbEngine,
    2:MysqlEngine,
}

def auto_connect(db_id):
    try:
        from dmp.models import Database
        db = Database.get(db_id)
        Engine = engines.get(db.db_type)
        conn = Engine(host=db.db_host,port=db.db_port,user=db.db_username,passwd=db.db_passwd,db=db.db_name)
        return  conn
    except Exception as e:
        raise e



def create_table_query_hanlder(table_name,fields):
     temp = "create table {table_name}(id int  auto_increment primary key{columns});"
     columns = "".join([",%s text"%col if col.strip() or col=="id" else ",None_"+col+"_%d text"%i for i,col in enumerate(fields)   ])
     return temp.format(table_name=table_name,columns=columns)