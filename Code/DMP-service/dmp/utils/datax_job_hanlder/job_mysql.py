#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/25
# @Author  : SHTD

import os
import json

def mysql_reader(username,password,column,host,port,db,table,where):
    """
    mysql数据读取者构造器
    :param username: str,数据库用户名,必填
    :param password: str,数据库密码,必填
    :param column: list,需要同步的列,非必填默认为所有
    :param host: str,数据库主机IP,必填
    :param port: int,数据库端口,必填
    :param db: str,数据库名称,必填
    :param table: str,数据表名称,必填
    :param where: str,筛选条件,非必填
    :return:
    """

    mysql_reader_josn = {
        "name": "mysqlreader",
        "parameter": {
            "username": username,
            "password": password,
            "column": column,
            "connection": [
                {
                "jdbcUrl": ["jdbc:mysql://%s:%d/%s"%(host,port,db)],
                "table": [table]
                }
            ],
            "where": where
            }
        }
    return mysql_reader_josn

def mysql_writer(model,username,password,column,host,port,db,table):
    """
    mysql数据写入者构造器
    :param model: int，写入模式，必填 1 insert 2 replace 3 update
    :param username: str,数据库用户名,必填
    :param password: str,数据库密码,必填
    :param column: list,需要同步的列,非必填默认为所有
    :param host: str,数据库主机IP,必填
    :param port: int,数据库端口,必填
    :param db: str,数据库名称,必填
    :param table: str,数据表名称,必填

    :return:
    """

    model_dict = {
        1:"insert",
        2:"replace",
        3:"update",
    }
    mysql_writer_json = {
        "name":"mysqlwriter",
        "parameter":{
            "writeMode": model_dict.get(model),
            "username": username,
            "password": password,
            "column": column,
            "connection": [
                {
                    "jdbcUrl": "jdbc:mysql://%s:%d/%s"%(host,port,db),
                    "table": [
                        table
                    ]
                }
            ]
        }
    }
    return mysql_writer_json
