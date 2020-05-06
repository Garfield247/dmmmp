#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from flask import Blueprint,jsonify

main = Blueprint("mian",__name__)

@main.route("/")
def test():
    result = {
        "status": 0,
        "msg": "success",
        "results":{
            "res":"OK",
        }
}
    return jsonify(result)