#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD

import pymongo
from flask import current_app


class MongodbEngine():

    type = 3
    def __init__(self, host, port, user, passwd, db):
        try:
            self.connect = pymongo.MongoClient(
                host=host, port=port, username=user, password=passwd)
            current_app.logger.info(self.connect.server_info())
            self.database = self.connect[db]
        except Exception as e:
            current_app.logger.error(
                "Connect Failed,Error Message:%s" % str(e))

    @property
    def tables_list(self):
        res = self.database.collection_names()
        # data
        return res

    def columns(self, collection):
        collection_ = self.database[collection]
        column_list = [
            {"dmp_data_table_column_name": str(
                k), "dmp_data_table_column_type": "Array" if type(v) == list else "string"}
            for k, v in
            collection_.find().limit(1)[0].items() if
            k != "_id"]
        return column_list

    def count(self, collection):
        return int(self.database[collection].count())

    def exec_query(self,**kwages):
        collection=kwages.get("collection")
        print(kwages)
        try:
            filters_str = kwages.get("filters") if  kwages.get("filters") else '{}'
            projection_str = kwages.get("projection") if kwages.get("projection") else  '{"_id": 0}'
            sort_str = kwages.get("sort") if  kwages.get("sort") else '[("_id", 1)]'
            print(filters_str, projection_str , sort_str)
            filters=eval(filters_str)
            projection=eval(projection_str)
            sort=eval(sort_str)
        except Exception as e:
            print(e)
            raise Exception("查询参数解析异常")
        skip=kwages.get("skip",0)
        limit=kwages.get("limit",100)

        res = self.database[collection].find(filters, projection).sort(
            sort).skip(skip).limit(limit)
        data = [r for r in res]
        return data

    def retrieve(self, table_name, limit=100):
        collection_ = self.database[table_name]
        res_ = collection_.find({}, {"_id": 0}).limit(100)
        data = [r for r in res_]
        return data

    def del_table(self, table_name):
        collection_ = self.database[table_name]
        collection_.drop()

    def close_conn(self):
        self.connect.close()
