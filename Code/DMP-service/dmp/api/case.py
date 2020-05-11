#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from flask import Blueprint, jsonify, request, current_app

from dmp.extensions import db
from dmp.models import Case,DataTable

case = Blueprint("case",__name__)

@case.route("/all/",methods=["GET"],defaults={"desc":"案例列表"})
def all(desc):
    """获取案例信息"""
    cases = list([c.__json__() for c in Case.query.all()])
    current_app.logger.info(dir(cases))
    # current_app.logger.info(cases.__json__())
    result = {
        "status": 0,
        "msg": "ok",
        "results":cases
    }

    return jsonify(result)

@case.route("/post/",methods=["POST"],defaults={"desc":"添加、修改案例"})
def cpost(desc):
    """添加修改案例"""
    if request.method == "POST":
        data = request.json
        if not data.get("case_id"):
            try:
                current_app.logger.info(request.json)
                case = Case(
                    dmp_case_name = data.get("dmp_case_name"),
                    description = data.get("description"),
                    url = data.get("url"),
                    url_name = data.get("url_name")
                )
                db.session.add(case)
                db.session.commit()
                current_app.logger.info("add case")
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
        elif data.get("case_id"):
            pass

@case.route("/del/",methods=["DELETE"],defaults={"desc":"删除案例"})
def cdel(desc):
    del_case_id = request.json.get("case_id")
    current_app.logger.info("del case , case_id :%d"%del_case_id)
    try:
        if DataTable.query.filter_by(dmp_case_id=del_case_id).count()<=0:
            del_case = Case.query.get(del_case_id)
            del_case.delete()
        result = {
            "status": 0,
            "msg": "ok",
            "results": {
                "ok":"OK!"
            }
        }
        return jsonify(result)
    except Exception as err:
        result = {
            "status": 203,
            "msg": "err",
            "results": {
                "error":str(err)
            }
        }
        return result


