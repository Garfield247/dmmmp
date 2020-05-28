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
    '''
     说明:获取用户组信息接口
     参数:Authorization,说明:用户标识信息token，管理员具有的权限,数据类型:String
     返回值:成功返回状态码、对应提示信息及所有用户组信息,数据类型:JSON,数据格式:{'msg':'...','results':[{'x':'x'},...],'status':xxx}
     '''
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
@usergroup.route("/grouplist/", methods=["GET"], defaults={"desc": "获取当前用户组信息"})
def grouplist(desc):
    '''
     说明:获取当前用户组信息接口
     参数:Authorization,dmp_group_id,说明:用户标识信息token，dmp_group_id为指定的用户组,数据类型:JSON
     返回值:成功返回状态码、对应提示信息及所有用户组信息,数据类型:JSON,数据格式:{'msg':'...','results':[{'x':'x'},...],'status':xxx}
     '''
    if request.method == 'GET':
        # 获取当前编辑用户组及用户组对应的权限所有信息
        try:
            data = request.json
            if data == None:
                return resp_hanlder(code=999)
            dmp_group_id = data.get('dmp_group_id')
            current_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
            current_group_permission_list = current_group_obj.permissions
            current_group_obj_dict = EnvelopedData.grouplist(current_group_permission_list, current_group_obj)
            return resp_hanlder(code=5002, msg=RET.alert_code[5002], result=current_group_obj_dict)
        except Exception as err:
            return resp_hanlder(code=999, err=err)


# +
@usergroup.route("/editgroup/", methods=["PUT"], defaults={"desc": "编辑用户组信息"})
def editgroup(desc):
    '''
     说明:编辑用户组信息接口
     参数:Authorization,dmp_group_id,dmp_group_name,max_count,dmp_permission,creator
          说明:用户标识信息token,dmp_group_id为选定的用户组,dmp_group_name为用户组名,max_count为用户组最大容量,
          dmp_permission为用户组对应的权限,creator为创建者,若有creator参数则选择,没有creator则默认为当前登录的用户,数据类型:JSON
     返回值:成功返回状态码、对应提示信息及编辑后的用户组信息,数据类型:JSON,数据格式:{'msg':'...','results':[{'x':'x'},...],'status':xxx}
     '''
    if request.method == 'PUT':
        # 编辑用户组
        try:
            data = request.json
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            dmp_group_id = data.get('dmp_group_id')
            dmp_group_name = data.get('dmp_group_name')
            max_count = data.get('max_count')
            dmp_permission_str = data.get('dmp_permission')
            creator = data.get('creator')
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


@usergroup.route("/post/", methods=["POST"], defaults={"desc": "添加用户组"})
def post(desc):
    '''
     说明:添加用户组接口
     参数:Authorization,dmp_group_name,max_count,creator,dmp_permission
          说明:用户标识信息token,dmp_group_name为用户组名,max_count为用户组最大容量,不允许给管理员用户组设置最大容量
          dmp_permission为用户组对应的权限,creator为创建者,若有creator参数则选择,没有creator则默认为当前登录的用户,数据类型:JSON
     返回值:成功返回状态码、对应提示信息及添加的用户组信息,数据类型:JSON,数据格式:{'msg':'...','results':{'x':'x'},'status':xxx}
     '''
    if request.method == 'POST':
        # 添加用户组
        try:
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            data = request.json
            dmp_group_name = data.get('dmp_group_name')
            max_count = data.get('max_count')
            creator = data.get('creator')
            dmp_permission_str = data.get('dmp_permission')
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
    '''
     说明:删除用户组接口
     参数:Authorization,dmp_group_id,说明:删除指定
          dmp_permission为用户组对应的权限,creator为创建者,若有creator参数则选择,没有creator则默认为当前登录的用户,数据类型:JSON
     返回值:成功返回状态码、对应提示信息及添加的用户组信息,数据类型:JSON,数据格式:{'msg':'...','results':{'x':'x'},'status':xxx}
     '''
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
