#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD

import re
from flask import current_app
from pyhive import hive


class HiveEngone():

    type=1
    def __init__(self, host, port, user, passwd, db):
        self.db = db
        try:
            self.conn = hive.Connection(host=host, port=port, username=user, password=passwd,
                                        database=db)
            current_app.logger.info(self.conn.client)
        except Exception as e:
            current_app.logger.error("Connect Failed! Error Message：%s" % str(e))

    @property
    def tables_list(self):
        cursor = self.conn.cursor()
        sql = """
        show tables
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        result = [i[0] for i in res]
        return result

    def columns(self, table_name):
        cursor = self.conn.cursor()
        sql = """
        desc {table_name}
        """
        cursor.execute(sql.format(table_name=table_name))
        _d = cursor.fetchall()
        columns_type_list = [{"dmp_data_table_column_name": str(column), "dmp_data_table_column_type": type} for
                             column, type, comment in _d]
        return columns_type_list

    def count(self, table_name):
        cursor = self.conn.cursor()
        sql = """
        select count(1) from {db}.{table_name}
        """
        cursor.execute(sql.format(db=self.db, table_name=table_name))
        _count = cursor.fetchall()
        return int(_count[0][0])

    def execsql(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def exec_query(self,**kwargs):
        sql = kwargs.get("sql")
        # limit = kwargs.get("limit", 100)
        # if not re.search(r"limit\s+\d+", sql,re.IGNORECASE):
            # if limit:
                # sql+" limit %d"%limit
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            return res
        except Exception as e:
            return str(e)

    def retrieve(self, table_name, limit=100):
        cursor = self.conn.cursor()
        sql = """
        Select * from {table_name}  limit {limit}
        """
        cursor.execute(sql.format(table_name=table_name, limit=limit))
        res = cursor.fetchall()
        return res

    def close_conn(self):
        self.conn.close()
