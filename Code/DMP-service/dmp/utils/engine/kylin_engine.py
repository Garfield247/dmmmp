#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/10/20
# @Author  : SHTD

import re
from flask import current_app
from dmp.utils.kylintool import KylinTool




class KylinEngin():
    type=4

    def __init__(self, host, port, user, passwd, db):
        self.kt = KylinTool(host=host, port= port, user= user, passwd=passwd)
        self.project = db

    def columns(self, table_name):
        # res = self.kt.api_get_cube_descriptor()
        pass


    def exec_query(self, **kwages):
        sql = kwages.get("sql")
        offset = kwages.get("offset",0)
        limit = kwages.get("limit", 100)
        project = self.project
        q = self.kt.api_query(sql=sql, offset=offset, limit=limit, project=self.project)

        result = q.get("results")
        return result
