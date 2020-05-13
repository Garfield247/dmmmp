#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from flask import Blueprint, jsonify, request, session

from dmp.extensions import db
from dmp.models import Groups, Permissions

usergroup = Blueprint("usergroup", __name__)


@usergroup.route("/info/", methods=["GET"])
def info():
    # 获取所有用户组信息及用户组对应的权限
    groups_all = Groups.query.all()
    groups_list = []
    for per_group_obj in groups_all:
        groups_list.append(per_group_obj)
    res_group_list = [g.group_to_dict() for g in groups_list]
    d = {}
    for item in groups_all:
        dmp_permission_list = []
        for p in item.permissions:
            p_dict = {}
            p_dict['id'] = p.id
            p_dict['route'] = p.route
            p_dict['dmp_permission_name'] = p.dmp_permission_name
            dmp_permission_list.append(p_dict)
        d[item.id] = dmp_permission_list

    for g in res_group_list:
        for key in d.keys():
            if g.get('id') == key:
                g['dmp_permission'] = d[key]
    return jsonify({
        'status': 0,
        'msg': 'Gets user group information and its corresponding permission information',
        'results': res_group_list
    })


# +
@usergroup.route("/grouplist/", methods=["GET"])
# 获取当前编辑用户组的所有信息
def grouplist():
    dmp_group_id = request.form.get('dmp_group_id')
    current_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
    current_group_permission_list = current_group_obj.permissions
    p_list = []
    for p in current_group_permission_list:
        if len(current_group_permission_list) == 0:
            break
        p_list.append(p.permission_to_dict())
    current_group_obj_dict = current_group_obj.group_to_dict()
    creator = session.get('creator')
    current_group_obj_dict['group_permission'] = p_list
    current_group_obj_dict['creator'] = creator
    return jsonify({
        'status': 0,
        'msg': 'User group information to be edited',
        'results': current_group_obj_dict
    })


# +
@usergroup.route("/editgroup/", methods=["POST"])
def editgroup():
    # 编辑用户组
    try:
        dmp_group_id = request.form.get('dmp_group_id')
        dmp_group_name = request.form.get('dmp_group_name')
        max_count = request.form.get('max_count')
        dmp_permission_str = request.form.getlist('dmp_permission')
        creator = request.form.get('creator')
        dmp_permission_list = [int(p) for p in dmp_permission_str]

        if int(dmp_group_id) == 1:
            return jsonify({
                'status': -1,
                'msg': 'The maximum capacity of the administrator user group cannot be modified',
                'results': {}
            })
        edit_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
        edit_group_obj.dmp_group_name = dmp_group_name
        edit_group_obj.max_count = max_count
        ret_data = edit_group_obj.group_to_dict()
        if creator:
            ret_data['creator'] = creator
        else:
            current_user_dict = session.get('user')
            creator = current_user_dict.get('dmp_username')
            ret_data['creator'] = creator

        db.session.add(edit_group_obj)
        db.session.commit()

        edit_permission_list = []
        for p in dmp_permission_list:
            if len(dmp_permission_list) == 0:
                break
            p_obj = Permissions.query.filter(Permissions.id == p).first()
            edit_permission_list.append(p_obj)

        # 用户组所对应数据库中的权限信息，根据Groups表中的dmp_group_name找到对应用户组的权限
        edit_group_obj = Groups.query.filter(Groups.dmp_group_name == dmp_group_name).first()
        edit_permission_obj_list = edit_group_obj.permissions
        # 清除原数据库表中该用户组所有的权限信息，保证内存指向相同
        edit_permission_obj_list.clear()
        # 然后添加勾选的权限信息对象
        for add_permission in edit_permission_list:
            edit_permission_obj_list.append(add_permission)

        group_pemission_list = []
        for p in edit_permission_obj_list:
            group_pemission_list.append(p.permission_to_dict())
        ret_data['group_permission'] = group_pemission_list

        return jsonify({
            'status': 0,
            'msg': 'User group edited successfully',
            'results': ret_data
        })
    except Exception:
        db.session.rollback()
        return jsonify({
            'status': -1,
            'msg': 'User group name is unique, please select again',
            'results': {}
        })


@usergroup.route("/post/", methods=["POST"])
def post():
    # 添加用户组
    try:
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

        ret_data = group_obj.group_to_dict()
        if creator:
            ret_data['creator'] = creator
        else:
            current_user_dict = session.get('user')
            creator = current_user_dict.get('dmp_username')
            ret_data['creator'] = creator

        # 用户勾选的权限，并在数据库权限表中找到对应的权限信息对象
        add_permission_list = []
        for p in dmp_permission_list:
            if len(dmp_permission_list) == 0:
                break
            p_obj = Permissions.query.filter(Permissions.id == p).first()
            add_permission_list.append(p_obj)

        # 用户组所对应数据库中的权限信息，根据Groups表中的dmp_group_name找到对应用户组的权限
        add_group_obj = Groups.query.filter(Groups.dmp_group_name == dmp_group_name).first()
        add_permission_obj_list = add_group_obj.permissions

        # 清除原数据库表中该用户组所有的权限信息，保证内存指向相同
        add_permission_obj_list.clear()
        # 然后添加勾选的权限信息对象
        for add_permission in add_permission_list:
            add_permission_obj_list.append(add_permission)

        group_pemission_list = []
        for p in add_permission_obj_list:
            group_pemission_list.append(p.permission_to_dict())
        ret_data['group_permission'] = group_pemission_list

        result = {
            'status': 0,
            'msg': 'User group and corresponding permissions were added successfully',
            'results': ret_data
        }
        return jsonify(result)

    except Exception:
        db.session.rollback()
        return jsonify({
            'status': -1,
            'msg': 'User group name is unique, please select again',
            'results': {}
        })


@usergroup.route("/del/", methods=["POST"])
def ugdel():
    # 删除用户组
    dmp_group_id = request.form.get('dmp_group_id')
    del_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
    db.session.delete(del_group_obj)
    db.session.commit()
    return jsonify({
        'status': 0,
        'msg': 'Group deletion successful',
        'results': {}
    })
