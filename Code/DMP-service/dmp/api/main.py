#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from flask import (Blueprint,
                   jsonify,
                   current_app
                   )
from dmp.utils.task import add
from dmp.models import *
from dmp.extensions import db

main = Blueprint("mian", __name__)


@main.route("/", defaults={"desc": "服务跟路由"})
def test(desc):
    db.create_all()
    result = {
        "status": 0,
        "msg": "success",
        "results": "DMP_SERVERS"
    }
    return jsonify(result)


@main.route("/apilist", defaults={"desc": "API列表"})
def apilist(desc):
    current_app.logger.info(current_app.url_map)
    return str(current_app.url_map)


@main.route('/testAdd', methods=["GET"], defaults={"desc": "celery测试路由"})
def test_add(desc):
    """
    测试相加
    :return:
    """
    result = add.delay(1, 2)
    res = result.get(timeout=1)
    data = {
        "status": 0,
        "msg": "success",
        "results": {
            "res": res,
        }}
    return jsonify(data)
