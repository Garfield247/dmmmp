#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from flask import Blueprint,jsonify

file = Blueprint("file",__name__)

@file.route("/upload/",methods=["POST"],defaults={"desc":"文件上传"})
def upload():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@file.route("/success/",methods=["GET"],defaults={"desc":"文件上传完成"})
def success():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@file.route("/dlcomplete/",methods=["GET"],defaults={"desc":"文件下载完成"})
def dlcomplete():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)