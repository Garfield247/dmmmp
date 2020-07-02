#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/25
# @Author  : SHTD 

def mongodb_reader(host, port, db_name, collection_name, column, username=None, password=None):
    mongodb_reader_json = {
        "name": "mongodbreader",
        "parameter": {
            "address": ["%s:%d" % (host, port)],
            "userName": username,
            "userPassword": password,
            "dbName": db_name,
            "collectionName": collection_name,
            "column": column,
        }}
    return mongodb_reader_json


def mongodb_writer(host, port, username, password, db_name, collection_name, column):
    """

    :param host:
    :param port:
    :param username:
    :param password:
    :param db_name:
    :param collection_name:
    :param column: list[{"name":"","type":"string"}] 数据列信息，必填
    :return:
    """
    mongodb_writer_json = {
        "name": "mongodbwriter",
        "parameter": {
            "address": [
                "%s:%d" % (host, port)
            ],
            "userName": username,
            "userPassword": password,
            "dbName": db_name,
            "collectionName": collection_name,
            "column": column,
        }
    }
    return mongodb_writer_json
