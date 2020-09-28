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
    """
    This is the language awesomeness API
    Call this api passing a language name and get back its features
    ---
    tags:
      - Awesomeness Language API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]
	"""
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

# @main.route("/spec")
# def spec():
    # # from flask_swagger import swagger
    # from flasgger import Swagger
    # swagger = Swagger(current_app)
    # return jsonify(swagger(current_app))
