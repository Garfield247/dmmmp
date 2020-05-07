#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from flask import Blueprint,jsonify
from dmp.utils.task import add
from dmp.models import *
from dmp.extensions import db

main = Blueprint("mian",__name__)

@main.route("/")
def test():
    db.create_all()
    result = {
        "status": 0,
        "msg": "success",
        "results":{
        }
}
    return jsonify(result)

@main.route("/cccc")
def teccccst():
    db.create_all()
    result = {
        "status": 0,
        "msg": "success",
        "results":{
            "res":"OK",
        }
}
    return jsonify(result)

@main.route('/testAdd', methods=["GET"])
def test_add():
    """
    测试相加
    :return:
    """
    result = add.delay(1, 2)
    res = result.get(timeout=1)
    data = {
        "status": 0,
        "msg": "success",
        "results":{
            "res":res,
        }}
    return jsonify(data)
