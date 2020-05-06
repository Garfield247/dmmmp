#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from flask import Blueprint,jsonify

user = Blueprint("user",__name__)

@user.route("/register/",method=["POST"])
def register():
    result = {
        "status": 0,
        "msg": "success",
        "results":{
        }
    }
    return jsonify(result)

@user.route("/activate/",method=["POST"])
def activate():
    result = {
        "status": 0,
        "msg": "success",
        "results":{
        }
    }
    return jsonify(result)

@user.route("/login/",method=["POST"])
def login():
    result = {
        "status": 0,
        "msg": "success",
        "results":{
            "token":"1312dasd312dcsdd31r3c"
        }
    }
    return jsonify(result)

@user.route("/forgetpwd/",method=["POST"])
def forgetpwd():
    result = {
        "status": 0,
        "msg": "success",
        "results":{
        }
    }
    return jsonify(result)

@user.route("/changepwd/",method=["PUT"])
def changepwd():
    result = {
        "status": 0,
        "msg": "success",
        "results":{
        }
    }
    return jsonify(result)

@user.route("/info/",method=["get"])
def info():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
            "id": "01",
            "dmp_username": "user01",
            "real_name": "user01",
            "email": "user01@test.com",
            "dmp_group": "admin",
            "leader_dmp_user": "admin",
            "user_info": "test_user",
            "last_login": "2020-04-21 09:00:00",
            "created_on": "2020-02-21 09:00:00",
            "changed_on": "2020-03-21 09:00:00",
        }
    }
    return jsonify(result)

@user.route("/icon/",method=["POST"])
def icon():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@user.route("/changeprofile/",method=["PUT"])
def changeprofile():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@user.route("/list/",method=["GET"])
def ulist():
    result = {
    "status": 0,
    "msg": "ok",
    "results":{
        "user01":{
            "id":"01",
            "dmp_username":"user01",
            "real_name":"user01",
            "email":"user01@test.com",
            "dmp_group":"stu",
            "leader_dmp_user_id":1,
            "user_info":"test_user",
            "last_login":"2020-04-21 09:00:00",
            "created_on":"2020-02-21 09:00:00",
            "changed_on":"2020-03-21 09:00:00",
        },
        "user02":{
            "id":"02",
            "dmp_username":"user02",
            "real_name":"user02",
            "email":"user02@test.com",
            "dmp_group":"stu",
            "leader_dmp_user_id":1,
            "user_info":"test_user",
            "last_login":"2020-04-21 09:00:00",
            "created_on":"2020-02-21 09:00:00",
            "changed_on":"2020-03-21 09:00:00",
        }}}

    return jsonify(result)

@user.route("/del/",method=["DEL"])
def udel():
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
            "del":"OK"
        }
    }
    return jsonify(result)