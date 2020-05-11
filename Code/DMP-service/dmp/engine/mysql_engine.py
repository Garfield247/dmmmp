#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD 

import pymysql


class MysqlEngine():

    def connect(self,host,port,user,passwd,db):

        try:
            conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
            cursor = conn.cursor()
            cursor.execute("select * from course")
            data = cursor.fetchall()
            for i in data:
                print('ID : '+str(i[0])+' NAME : '+i[1]+' TEACHER : '+str(i[2]))
            cursor.close()
            conn.close()
        except Exception:
            print('发生异常')

    def test_connect(self):
        try:
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='school')
            cursor = conn.cursor()
            cursor.execute("select * from course")
            data = cursor.fetchall()
            for i in data:
                print('ID : '+str(i[0])+' NAME : '+i[1]+' TEACHER : '+str(i[2]))
            cursor.close()
            conn.close()
        except Exception:
            print('发生异常')
