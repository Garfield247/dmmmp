#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/10/20
# @Author  : SHTD

import re
from flask import current_app
from dmp.utils.kylintool import KylinTool




class KylinEngin():
    def __init__(self):
        self.kt = KylinTool(
            host = current_app.config.get("KYLIN_HOST"),
            port = current_app.config.get("KYLIN_PORT"),
            user = current_app.config.get("KYLIN_USER"),
            pswd= current_app.config.get("KYLIN_PASSWD")
            )
        self.project = current_app.config.get("KYLIN_PROJECT")

    def exec_query(self, **kwages):
        sql = kwages.get("sql")
        offset = kwages.get("offset",0)
        limit = kwages.get("limit", 100)
        project = self.project
        q = self.kt.api_query(sql=sql, offset=offset, limit=limit, project=project)

        result = q.get("results")
        return result
