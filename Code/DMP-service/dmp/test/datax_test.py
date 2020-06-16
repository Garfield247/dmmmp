#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/25
# @Author  : SHTD 


from flask import current_app
from dmp.utils.datax_job_hanlder import mongodb_reader,mysql_writer
from dmp.utils.job_task import job_hanlder
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

