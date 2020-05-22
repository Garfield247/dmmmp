#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from flask import Blueprint, request

from dmp.extensions import db
from dmp.models import Groups, Users
from dmp.utils.put_data import PuttingData
from dmp.utils.response_hanlder import resp_hanlder, RET
from dmp.utils.ep_data import EnvelopedData

usergroup = Blueprint("usergroup", __name__)


@usergroup.route("/info/", methods=["GET"], defaults={"desc": "获取用户组信息"})
def info(desc):
    if request.method == 'GET':
        # 获取所有用户组信息及用户组对应的权限
        groups_all = Groups.query.all()
        res_group_list, d = EnvelopedData.usergroup_info(groups_all)
        for g in res_group_list:
            for key in d.keys():
                if g.get('id') == key:
                    g['dmp_permission'] = d[key]
        return resp_hanlder(code=5001, msg=RET.alert_code[5001], result=res_group_list)


# +
@usergroup.route("/grouplist/", methods=["GET"])
def grouplist():
    if request.method == 'GET':
        # 获取当前编辑用户组及用户组对应的权限所有信息
        try:
            data = request.json
            dmp_group_id = data.get('dmp_group_id')
            current_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
            current_group_permission_list = current_group_obj.permissions
            current_group_obj_dict = EnvelopedData.grouplist(current_group_permission_list, current_group_obj)
            return resp_hanlder(code=5002, msg=RET.alert_code[5002], result=current_group_obj_dict)
        except Exception as err:
            return resp_hanlder(code=999, err=err)


# +
@usergroup.route("/editgroup/", methods=["POST"])
def editgroup():
    if request.method == 'POST':
        # 编辑用户组
        try:
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            dmp_group_id = request.form.get('dmp_group_id')
            dmp_group_name = request.form.get('dmp_group_name')
            max_count = request.form.get('max_count')
            dmp_permission_str = request.form.getlist('dmp_permission')
            creator = request.form.get('creator')
            dmp_permission_list = [int(p) for p in dmp_permission_str]
            # 管理员的最大容量就等于数据库原始定义的容量，不受参数而改变
            if dmp_group_name == 'root':
                db_max_count = Groups.query.filter(Groups.dmp_group_name == dmp_group_name).first().max_count
                max_count = db_max_count
            edit_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
            edit_group_obj.dmp_group_name = dmp_group_name
            edit_group_obj.max_count = max_count
            ret_data = EnvelopedData.post_edit(res, edit_group_obj, creator, dmp_permission_list, dmp_group_name)
            return resp_hanlder(code=5004, msg=RET.alert_code[5004], result=ret_data)
        except Exception as err:
            db.session.rollback()
            return resp_hanlder(code=999, err=err)


@usergroup.route("/post/", methods=["POST"], defaults={"desc": "修改添加用户组"})
def post(desc):
    if request.method == 'POST':
        # 添加用户组
        try:
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)

            dmp_group_name = request.form.get('dmp_group_name')
            max_count = request.form.get('max_count')
            creator = request.form.get('creator')
            dmp_permission_str = request.form.getlist('dmp_permission')
            dmp_permission_list = [int(p) for p in dmp_permission_str]
            # 不允许给管理员设置最大用户组容量，默认为3个，创建管理员时已进行设置判断
            if dmp_group_name == 'root':
                max_count = None
            group_obj = Groups(dmp_group_name=dmp_group_name, max_count=max_count)
            db.session.add(group_obj)
            db.session.commit()
            ret_data = EnvelopedData.post_edit(res, group_obj, creator, dmp_permission_list, dmp_group_name)
            return resp_hanlder(code=5005, msg=RET.alert_code[5005], result=ret_data)
        except Exception as err:
            db.session.rollback()
            return resp_hanlder(code=999, err=err)


@usergroup.route("/del/", methods=["DELETE"], defaults={"desc": "删除用户组"})
def ugdel(desc):
    if request.method == 'DELETE':
        # 删除用户组
        try:
            dmp_group_id = request.form.get('dmp_group_id')
            del_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
            db.session.delete(del_group_obj)
            db.session.commit()
            return resp_hanlder(code=5007, msg=RET.alert_code[5007])
        except Exception as err:
            return resp_hanlder(code=999, err=err)
