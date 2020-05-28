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





    def close_conn(self):
        self.conn.close()