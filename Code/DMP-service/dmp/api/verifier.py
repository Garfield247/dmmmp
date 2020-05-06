  
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from flask import Blueprint,jsonify

verifier = Blueprint("verifier",__name__)

@verifier.route("/email/",method=["GET"])
def email():
    result = {
        "status": 0,
        "msg": "success",
        "results":{
            "exist":False,
        }
    }
    return jsonify(result)

@verifier.route("/username/",method=["GET"])
def username():
    result = {
        "status": 0,
        "msg": "success",
        "results":{
            "exist":False,
        }
    }
    return jsonify(result)