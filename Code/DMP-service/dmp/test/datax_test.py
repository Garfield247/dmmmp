#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/25
# @Author  : SHTD

import os
from hdfs import Client
from flask import current_app
import pandas as pd
from dmp.utils.datax_job_hanlder import mongodb_reader,mysql_writer,textfile_reader,textfile_writer,hive_reader,hive_writer
from dmp.utils.job_task import job_hanlder
from dmp.utils import uuid_str
import datetime
# from dmp.utils.engine import create_table_query_hanlder
def test():
    mongo_cloumn = [{"index": 1, "name": "job_name", "type": "string"},
                                                       {"index": 2, "name": "tag", "type": "string"},
                                                       {"index": 3, "name": "position", "type": "string"},
                                                       {"index": 4, "name": "crawl_date", "type": "string"},
                                                       {"index": 5, "name": "job_category", "type": "string"},
                                                       {"index": 6, "name": "company_name", "type": "string"},
                                                       {"index": 7, "name": "company_scale", "type": "string"},
                                                       {"index": 8, "name": "company_addr", "type": "string"},
                                                       {"index": 9, "name": "salary", "type": "string"},
                                                       {"index": 10, "name": "edu", "type": "string"},
                                                       {"index": 11, "name": "experience", "type": "string"},
                                                       {"index": 12, "name": "job_info", "type": "string"},
                                                       {"index": 13, "name": "job_location", "type": "string"},
                                                       {"index": 14, "name": "source", "type": "string"}, ]
    r = mongodb_reader(host="192.168.3.119",port=27017,db_name="case01",collection_name="yingcai_data",username=None,password=None,column=mongo_cloumn)


    mysql_column = ["job_name", "tag", "position", "crawl_date",
                                                             "job_category", "company_name", "company_scale",
                                                             "company_addr", "salary", "edu", "experience", "job_info",
                                                             "job_location", "source"
                                                             ]
    w = mysql_writer(model=1,host="192.168.3.87",port=3306,username="root",password="shtd123.",column=mysql_column,db="dmo_test",table="test_yc",preSql=None,postSql=None)

    res = job_hanlder.delay(reader=r,writer=w)
    current_app.logger.info(res)

def test_csv2mysql():
    table_name = "testxxx"
    file_path = os.path.join(current_app.config.get("UPLOADED_PATH"), "hdy2.csv")
    csv_column = list(pd.read_csv(file_path, header=0).columns)
    csv_column_d = [{"index":i,"type":"string"}for i,cc in enumerate(csv_column)]
    r = textfile_reader(
        filepath=file_path,
        column=csv_column_d

    )
    preSql = create_table_query_hanlder(table_name=table_name,fields=csv_column)
    w = mysql_writer(model=1, host="192.168.3.87", port=3306, username="root", password="shtd123.", column=csv_column,
                     db="dmp_test", table="test_hdy", preSql=preSql, postSql=None)

    res = job_hanlder.delay(reader=r, writer=w)
    current_app.logger.info(res)

def test_csv2hive():

    table_name = "testxxx"
    hdfs_url = "http://{host}:{port}"
    hdfs_cli = Client(hdfs_url.format(host="192.168.3.140",port=50070))
    file_path = os.path.join(current_app.config.get("UPLOADED_PATH"), "hdy2.csv")
    csv_column = list(pd.read_csv(file_path, header=0).columns)
    csv_column_d = [{"index":i,"type":"string"}for i,cc in enumerate(csv_column)]
    r = textfile_reader(
        filepath=file_path,
        column=csv_column_d
    )

    fpath = "/dmp_cache/%s_data/%s_%s"%(str(datetime.datetime.now().date()),table_name,uuid_str())
    # fpath = "/dmp_cache/2020-06-23-data/testxxx_asda8937/"
    print(fpath)
    hdfs_cli.makedirs(hdfs_path=fpath,permission="775")
    hive_columns = [{"name":col,"type":"string"}for col in csv_column]
    w = hive_writer(host="192.168.3.140",port=8020,filename=table_name,path=fpath,column=hive_columns)

    res = job_hanlder.delay(reader=r, writer=w)
    current_app.logger.info(res)


def test_hive2csv():
    # col = ['siteCode', 'siteName', 'dateTime', 'pH', 'DO', 'NH4', 'CODMn', 'TOC', 'level', 'levelStatus', 'attribute',
    #  'status'
    #  ]
    # colu = [{}for c in col]
    r = hive_reader(host="192.168.3.140",port=8020,path="/user/hive/warehouse/test.db/test_hdy",fileType="text",column=["*"],fieldDelimiter=",")
    w = textfile_writer(filepath="./",filename="hdy_test.csv",header=0)
    res = job_hanlder.delay(reader=r, writer=w)
    current_app.logger.info(res)
