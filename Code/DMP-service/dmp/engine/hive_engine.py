#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD

from flask import current_app
from pyhive import hive


class HiveEngone():

    def __init__(self,host,port,user,passwd,db):
        try:
            self.connect = hive.Connection(host=host, port=port, username=user, password=password,
                                   database=db)
            current_app.logger.info(self.connect.__dict__)
        except Exception as e:
            current_app.logger.error("Connect Failed! Error Message：%s"%str(e))

    def tables_list(self):
        cursor = self.conn.cursor()
        sql = """
        show tables
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        result = [i[0] for i in res]
        return result
        
    def columns(self,table_name):
        cursor = self.connect.cursor()
        sql = """
        Select COLUMN_NAME column, DATA_TYPE type from INFORMATION_SCHEMA.COLUMNS Where table_name = '{table_name}';
        """
        cursor.execute(sql.format(table_name=table_name))
        _d = cursor.fetchall()
        columns_type_list = [ {"column":column,"type":type} for column,type in _d]
        return columns_type_list

    def count(self,table_name):
        cursor = self.connect.cursor()
        sql = """
        Select count(*) form {table_name};
        """
        cursor.execute(sql.format(table_name=table_name))
        _count = cursor.fetchall()
        return int(_count[0][0])



    def retrieve(self,table_name,where = "id > 0",limit=100):
        cursor = self.connect.cursor()
        sql = """
        Select * from {table_name } where {where } limit {limit};
        """
        cursor.execute(sql.format(table_name=table_name,where=where,limit=limit))
        res = cursor.fetchall()
        return res

    def close_conn(self):
        self.connect.close()
