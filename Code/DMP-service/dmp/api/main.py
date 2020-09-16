#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from datetime import datetime
from flask import (Blueprint,
                   jsonify,
                   current_app
                   )
from dmp.utils.job_task import add
from dmp.models import *
from dmp.extensions import db,apscheduler
from dmp.utils.aps_task import task2json

main = Blueprint("mian", __name__)


@main.route("/", defaults={"desc": {"interface_name": "服务跟路由","is_permission": False,"permission_belong": None}})
def test(desc):
    db.create_all()
    result = {
        "status": 0,
        "msg": "success",
        "results": "DMP_SERVERS"
    }
    return jsonify(result)
#
#
# @main.route("/apilist", defaults={"desc": {"interface_name": "API列表","is_permission": True,"permission_belong": 1}})
# def apilist(desc):
#     current_app.logger.info(current_app.url_map)
#     return str(current_app.url_map)
#
#
def say(word):
    print(word,datetime.now())

@main.route('/testAdd', methods=["GET"], defaults={"desc": {"interface_name": "celery测试路由","is_permission": True,"permission_belong": 1}})
def test_add(desc):
    """
    测试相加
    :return:
    """
    apscheduler.add_job(id="csawad",func=say,kwargs={"word":"hello"},trigger="interval",weeks=60)
    return "OK! "

@main.route("/tasks",methods=["GET"])
def tasks():
    jobs = apscheduler.get_jobs()
    res = [task2json(job) for job in apscheduler.get_jobs()]
    return {"res":res}

@main.route("/stopall",methods=["GET"])
def stops():
    apscheduler.delete_all_jobs()
    return {"res":"ok"}
