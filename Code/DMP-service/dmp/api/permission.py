#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from flask import Blueprint, jsonify, request
from dmp.models import Permissions

permission = Blueprint("permission",__name__)

@permission.route("/all/",methods=["GET"])
def all():
    # 获取当前所有权限信息
    permissions_all = Permissions.query.all()
    permissions_list = []
    for per_permission_obj in permissions_all:
        permissions_list.append(per_permission_obj)
    res_permission_list = [p.permission_to_dict() for p in permissions_list]

    result = {
        'status': 0,
        'msg': 'Returned all the permissions list',
        'results': res_permission_list
    }
    return jsonify(result)

