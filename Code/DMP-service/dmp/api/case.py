#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD


from flask import Blueprint, request, current_app

from dmp.models import Case, DataTable
from dmp.utils import resp_hanlder

case = Blueprint("case", __name__)


@case.route("/all/", methods=["GET"], defaults={"desc": {"interface_name": "案例列表","is_permission": True,"permission_belong": 1}})
def all(desc):
    """获取案例信息"""
    cases = list([c.__json__() for c in Case.query.all()])
    return resp_hanlder(result=cases)


@case.route("/post/", methods=["POST", "PUT"], defaults={"desc": {"interface_name": "添加、修改案例","is_permission": True,"permission_belong": 1}})
def cpost(desc):
    """添加修改案例"""
    case_info = request.json
    if request.method == "POST":
        if not case_info.get("case_id"):
            try:
                current_app.logger.info(request.json)
                new_case = Case(
                    dmp_case_name=case_info.get("dmp_case_name"),
                    description=case_info.get("description"),
                    url=case_info.get("url"),
                    url_name=case_info.get("url_name")
                )
                new_case.save()
                # current_app.logger.info("add case")
                return resp_hanlder(result="OK")
            except Exception as err:
                return resp_hanlder(code=202,err=err)
    elif request.method == "PUT":
        if case_info.get("case_id"):
            try:
                modify_case = Case.query.get(case_info.get("case_id"))
                # current_app.logger.info(modify_case)
                if "dmp_case_name" in case_info.keys():
                    modify_case.dmp_case_name = case_info.get("dmp_case_name")
                if "description" in case_info.keys():
                    modify_case.description = case_info.get("description")
                if "url" in case_info.keys():
                    modify_case.url = case_info.get("url")
                if "url_name" in case_info.keys():
                    modify_case.url_name = case_info.get("url_name")
                modify_case.put()
                # current_app.logger.info("修改完成")
                return resp_hanlder(result={"update": "OK!"})
            except Exception as err:
                return resp_hanlder(cdoe=203, err=err)


@case.route("/del/", methods=["DELETE"], defaults={"desc": {"interface_name": "删除案例","is_permission": True,"permission_belong": 2}})
def cdel(desc):
    del_case_id = request.json.get("case_id")
    current_app.logger.info("del case , case_id :%d" % del_case_id)
    try:
        del_case = Case.query.get(del_case_id)
        del_case.delete()
        return resp_hanlder(result="OK")
    except Exception as err:
        return resp_hanlder(code=203, err=err)
