#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from flask import Blueprint, jsonify, request, current_app

from dmp.extensions import db
from dmp.models import Case,DataTable
from dmp.utils import resp_hanlder

case = Blueprint("case",__name__)

@case.route("/all/",methods=["GET"],defaults={"desc":"案例列表"})
def all(desc):
    """获取案例信息"""
    cases = list([c.__json__() for c in Case.query.all()])
    current_app.logger.info(dir(cases))
    # current_app.logger.info(cases.__json__())
    return resp_hanlder(result=cases)

@case.route("/post/",methods=["POST","PUT"],defaults={"desc":"添加、修改案例"})
def cpost(desc):
    """添加修改案例"""
    data = request.json
    if request.method == "POST":
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
                return resp_hanlder(result="OK")
            except Exception as err:
                return resp_hanlder(code=202,err=err)
    if request.method == "PUT":
        if data.get("case_id"):
            try:
                case = Case.query.get(data.get("case_id"))
                current_app.logger.info(case)
                if data.get("dmp_case_name"):
                    case.dmp_case_name = data.get("dmp_case_name")
                if data.get("description"):
                    case.description = data.get("description")
                if data.get("url"):
                    case.url = data.get("url")
                if data.get("url_name"):
                    case.url_name = data.get("url_name")
                case.put()
                current_app.logger.info("修改完成")
                return resp_hanlder(result={"update":"OK!"})
            except Exception as err:
                return resp_hanlder(cdoe=203,err=err)


@case.route("/del/",methods=["DELETE"],defaults={"desc":"删除案例"})
def cdel(desc):
    del_case_id = request.json.get("case_id")
    current_app.logger.info("del case , case_id :%d"%del_case_id)
    try:
        if DataTable.query.filter_by(dmp_case_id=del_case_id).count()<=0:
            del_case = Case.query.get(del_case_id)
            del_case.delete()
        return resp_hanlder(result="OK")
    except Exception as err:
        return resp_hanlder(code=203,err=err)


