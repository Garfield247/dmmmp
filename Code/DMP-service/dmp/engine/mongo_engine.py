#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD

import pymongo
from flask import current_app


class MongodbEngine():

    def __init__(self, host, port, user, password, db):
        try:
            self.connect = pymongo.MongoClient(host=host, port=port, username=user, password=password)
            current_app.logger.info(self.connect.server_info())
            self.database = self.connect[db]
        except Exception as e:
            current_app.logger.error("Connect Failed,Error Message:%s" % str(e))

    def columns(self, collection):
        collection_ = self.database[collection]
        column_list = [{"column": k, "type": "Array" if type(v) == list else "string"} for k, v in
                       collection_.find().limit(1)[0].items() if
                       k != "_id"]
        return column_list


    def count(self,collection):
        return int(self.database[collection].count())

    def retrieve(self):
        pass

    def close_conn(self):
        self.connect.close()
