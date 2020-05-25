#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/25
# @Author  : SHTD

import os
import json

def mysql_reader(username,password,column,host,port,db,table,where,querySql):
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
    :param querySql: str,自定SQL语句，非必填
    :return:
    """

    mysql_reader_josn = {
        "name": "mysql_reader",
        "parameter": {
            "username": username,
            "password": password,
            "column": column if column else ["*"],
            "connection": [
                {
                "querySql": [querySql],
                "jdbcUrl": "jdbc:mysql://%s:%d/%s"%(host,port,db),
                "table": [table]
                }
            ],
            "where": where
            }
        }
    return mysql_reader_josn

def mysql_writer(model,username,password,column,host,port,db,table,preSql,postSql):
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
    :param preSql: list[str],数据写入前执行的SQL，非必填
    :param postSql: list[str],数据写入后执行的SQL语句，非必填
    :return:
    """

    model_dict = {
        1:"insert",
        2:"replace",
        3:"update",
    }
    mysql_writer_json = {
        "name":"mysql_writer",
        "parameter":{
            "writeMode": model_dict.get(model),
            "username": username,
            "password": password,
            "column": column if column else [""],
            "preSql": preSql,
            "postSql":postSql,
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
