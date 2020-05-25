#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/25
# @Author  : SHTD 


import os
from dmp.datax_job_hanlder import *
def test():
    r = mongodb_reader(host="192.168.3.119",port=27017,db_name="case01",collection_name="yingcai_data")
    w = mysql_writer(host="192.168.3.87",port=3306,db="database",table="test_yc")
    job_jsonpath = job_hanlder(reader=r,writer=w)

    os.system("python /root/datax/bin/datax.py %s"%job_jsonpath)