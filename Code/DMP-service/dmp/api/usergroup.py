#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from flask import Blueprint,jsonify

usergroup = Blueprint("usergroup",__name__)

@usergroup.route("/info/",method=["GET"])
def info():
    result = {
        "status": 0,
        "msg": "ok",
        "results":[
            {
            "id":1,
            "dmp_group_name":"group01",
            "max_count":1000,
            "created_on":"2020-03-09 12:00:00",
            "changed_on":"2020-04-09 12:00:00",
            "dmp_permission":["permission01","permission02","permission03","permission04"],
            "dmp_lights":["lights01","lights02","lights,03","lights04","lights05"],
            },
            {
            "id":2,
            "group_name":"group02",
            "max_count":1000,
            "created_on":"2020-03-09 12:00:00",
            "changed_on":"2020-04-09 12:00:00",
            "dmp_permission":["permission01","permission02","permission03","permission04"],
            "dmp_lights":["lights01","lights02","lights,03","lights04","lights05"],
            }
        ]
        }

    return jsonify(result)

@usergroup.route("/post/",method=["POST"])
def post():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)


@usergroup.route("/del/",method=["DEL"])
def ugdel():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)