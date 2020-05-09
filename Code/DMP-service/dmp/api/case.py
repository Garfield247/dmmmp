#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from flask import Blueprint, jsonify, request, current_app

from dmp.extensions import db
from dmp.models import Case

case = Blueprint("case",__name__)

@case.route("/all/",methods=["GET"],defaults={"desc":"案例列表"})
def all(desc):
    """
    获取案例信息
    :param desc:
    :return:
    """
    cases = list(Case.query.all())
    result = {
        "status": 0,
        "msg": "ok",
        "results":cases
    }

    return jsonify(result)

@case.route("/post/",methods=["POST"],defaults={"desc":"添加、修改案例"})
def cpost(desc):
    if request.method == "POST":
        if not request.args.get("case_id"):
            try:
                current_app.logger.info(request.json)
                case = Case(
                    dmp_case_name = request.form.get("dmp_case_name"),
                    description = request.form.get("description"),
                    url = request.form.get("url"),
                    url_name = request.form.get("url_name")
                )
                db.session.add(case)
                db.session.commit()
                result = {
                    "status":0,
                    "msg":"oK",
                    "result":"OK"
                }
                return jsonify(result)
            except Exception as err:
                result = {
                    "status": 202,
                    "msg": "error",
                    "results": {
                        "error":str(err)
                    }
                }
                return jsonify(result)
        elif request.form.get("case_id"):
            pass

@case.route("/del/",methods=["DEL"],defaults={"desc":"删除案例"})
def cdel(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)


