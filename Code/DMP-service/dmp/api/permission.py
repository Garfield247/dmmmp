#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from flask import Blueprint,jsonify

permission = Blueprint("permission",__name__)

@permission.route("/all/",methods=["GET"],defaults={"desc":"获取所有权限"})
def all(desc):
    result = {
    "status": 0,
    "msg": "ok",
    "results":[
        {
        "id":1,
        "permission":"permission211"
        },
        {
        "id":2,
        "permission":"permission2"
        }
    ]
    }
    return jsonify(result)