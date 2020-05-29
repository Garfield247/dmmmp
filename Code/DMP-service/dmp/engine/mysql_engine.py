#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD 

import pymysql
from flask import current_app

class MysqlEngine():

    def __int__(self,host,port,user,passwd,db):

        try:
            self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
            current_app.logger.info(self.conn.server_version)
        except Exception:
            current_app.logger.error('发生异常')

    def columns(self,table_name):
        cursor = self.conn.cursor()
        sql = """
        Select COLUMN_NAME column, DATA_TYPE type from INFORMATION_SCHEMA.COLUMNS Where table_name = '{table_name}';
        """
        cursor.execute(sql.format(table_name=table_name))
        _d = cursor.fetchall()
        columns_type_list = [ {"column":column,"type":type} for column,type in _d]
        return columns_type_list



    def close_conn(self):
        self.conn.close()