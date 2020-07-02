#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import Blueprint, request

from dmp.models import Permissions
from dmp.utils.response_hanlder import resp_hanlder, RET

permission = Blueprint("permission", __name__)


# @permission.route("/all/", methods=["GET"], defaults={"desc": "获取所有权限"})
@permission.route("/all/", methods=["GET"], defaults={"desc": {"interface_name": "获取所有权限",
                                                               "is_permission": True,
                                                               "permission_belong": 2}})
def all(desc):
    if request.method == 'GET':
        # 获取当前所有权限信息
        permissions_all = Permissions.query.all()
        permissions_list = []
        for per_permission_obj in permissions_all:
            permissions_list.append(per_permission_obj)
        res_permission_list = [p.permission_to_dict() for p in permissions_list]
        return resp_hanlder(code=6001, msg=RET.alert_code[6001], result=res_permission_list)
