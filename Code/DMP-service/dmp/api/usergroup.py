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



@usergroup.route("/info/", methods=["GET"], defaults={"desc": {"interface_name": "获取用户组信息","is_permission": True,"permission_belong": 2}})
def info(desc):
    '''
     说明:获取用户组信息接口
     参数:Authorization,说明:用户标识信息token，管理员具有的权限,数据类型:String
     返回值:成功返回状态码、对应提示信息及所有用户组信息,数据类型:JSON,数据格式:{'msg':'...','results':[{'x':'x'},...],'status':xxx}
     '''
    if request.method == 'GET':
        try:
            # +
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            if not isinstance(res, dict):
                return resp_hanlder(code=999)
            data = request.json
            if data == None:
                # 超级管理员可以获取所有用户组信息及用户组对应的权限，并选择添加
                if res.get('id') == 1:
                    groups_all = Groups.query.all()
                    res_group_list = EnvelopedData.return_group_list(groups_all)
                    return resp_hanlder(code=5001, msg=RET.alert_code[5001], result=res_group_list)

                # 普通管理员--获取低于此用户组的所有用户组信息，包括新添加的用户组的is_show=2 / is_show=3
                # 或者新添加的用户组属于管理员用户组分类，和普通管理员显示的用户组信息一样
                # 凡是可以进入此接口的必然是 超级管理员和普通管理员或者是属于管理员分类的用户组
                # 默认普通管理员
                if res.get('id') != 1:
                    except_admin_groups_list = Groups.query.filter(Groups.id != 1).all()  # 教师、学生及新添加
                    add_groups_list = Groups.query.filter(Groups.id != 1, Groups.id != 2, Groups.id != 3).all()
                    # 表示有新添加的用户组，需要判断is_show的值并返回
                    if len(add_groups_list) != None:
                        ag_dict = EnvelopedData.build_data_structures(add_groups_list)
                        for k, v in ag_dict.items():
                            is_show = EnvelopedData.estimate_classify(v)
                            # 除了管理员类别的新添加用户组
                            # is_show = 1,则表示为管理员类别组，不显示，移除
                            if is_show == 1:
                                except_admin_groups_list.remove(
                                    Groups.query.filter(Groups.id == k).first())
                                continue
                            else:
                                # 不进行操作
                                continue
                        res_group_list = EnvelopedData.return_group_list(except_admin_groups_list)
                        return resp_hanlder(code=5001, msg=RET.alert_code[5001], result=res_group_list)

                    else:
                        res_group_list = EnvelopedData.return_group_list(except_admin_groups_list)
                        return resp_hanlder(code=5001, msg=RET.alert_code[5001], result=res_group_list)
            else:
                dmp_group_id = data.get('dmp_group_id')
                current_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
                current_group_permission_list = current_group_obj.permissions
                current_group_obj_dict = EnvelopedData.grouplist(current_group_permission_list, current_group_obj)
                return resp_hanlder(code=5002, msg=RET.alert_code[5002], result=current_group_obj_dict)

        except Exception as err:
            return resp_hanlder(code=999, msg=str(err))

@usergroup.route("/belong/", methods=["GET"], defaults={"desc": {"interface_name": "获取用户分配用户组信息","is_permission": True,"permission_belong": 1}})
def belong(desc):
    if request.method == 'GET':
        try:
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            if not isinstance(res, dict):
                return resp_hanlder(code=999)
            data = request.json
            # 判断当前登录用户的is_show的值，如果is_show=2,则都显示，如果is_show=1,则属于教师组分类，则显示教师组以下的用户组，is_show=3，学生无法进入changeprofile接口
            # 超级管理员可以获取所有用户组信息，并选择添加
            if res.get('id') == 1:
                groups_all = Groups.query.all()
                res_group_list = EnvelopedData.return_group_list(groups_all)
                return resp_hanlder(code=5001, msg=RET.alert_code[5001], result=res_group_list)
            # 普通管理员---is_show=1,展示除了管理员用户组的所有用户组，在判断新添加的用户组所属类别
            if res.get('id') != 1 and res.get('dmp_group_id') == 1:
                except_admin_groups_list = Groups.query.filter(Groups.id != 1).all()  # 教师、学生及新添加
                add_groups_list = Groups.query.filter(Groups.id != 1, Groups.id != 2, Groups.id != 3).all()
                # 表示有新添加的用户组，需要判断is_show的值并返回
                if len(add_groups_list) != None:
                    ag_dict = EnvelopedData.build_data_structures(add_groups_list)
                    for k, v in ag_dict.items():
                        is_show = EnvelopedData.estimate_classify(v)
                        # 除了管理员类别的新添加用户组
                        # is_show = 1,则表示为管理员类别组，不显示，移除
                        if is_show == 1:
                            except_admin_groups_list.remove(
                                Groups.query.filter(Groups.id == k).first())
                            continue
                        else:
                            # 不进行操作
                            continue
                    res_group_list = EnvelopedData.return_group_list(except_admin_groups_list)
                    return resp_hanlder(code=5001, msg='Display all user group information successfully.', result=res_group_list)

                else:
                    res_group_list = EnvelopedData.return_group_list(except_admin_groups_list)
                    return resp_hanlder(code=5001, msg='Display all user group information successfully.', result=res_group_list)
            # 教师展示可分配用户组--展示教师用户组以下级别的用户组(student)，以及新添加的用户组is_show=0
            if res.get('dmp_group_id') == 2:
                except_teacher_groups_list = Groups.query.filter(Groups.id != 1, Groups.id != 2).all()  # 排除管理员、教师的用户组列表
                # 新添加的用户组，需要筛选is_show=0的用户组作为显示
                add_groups_list = Groups.query.filter(Groups.id != 1, Groups.id != 2, Groups.id != 3).all()
                if len(add_groups_list) != None:
                    ag_dict = EnvelopedData.build_data_structures(add_groups_list)
                    for k, v in ag_dict.items():
                        is_show = EnvelopedData.estimate_classify(v)
                        # 除了管理员类别的新添加用户组
                        # is_show = 1 或者 is_show = 2,则表示为管理员类别组或者教师类别组，不显示，移除
                        if is_show == 1 or is_show == 2:
                            except_teacher_groups_list.remove(
                                Groups.query.filter(Groups.id == k).first())
                            continue
                        else:
                            # 不进行操作
                            continue
                    res_group_list = EnvelopedData.return_group_list(except_teacher_groups_list)
                    return resp_hanlder(code=5001, msg='Display all user group information successfully.', result=res_group_list)
                else:
                    # 没有新添加的用户组，默认仅展示学生用户组
                    res_group_list = EnvelopedData.return_group_list(except_teacher_groups_list)
                    return resp_hanlder(code=5001, msg='Display all user group information successfully.', result=res_group_list)
            # 属于新添加用户组的用户登录--判断新添加的用户组的is_show的值，如果is_show=2--普通管理员，如果is_show=1--教师，如果is_show=3--学生，不考虑
            if res.get('dmp_group_id') != 1 and res.get('dmp_group_id') != 2 and res.get('dmp_group_id') != 3:
                add_group_obj = Groups.query.filter(Groups.id == res.get('dmp_group_id')).first()
                add_group_obj_list = []
                add_group_obj_list.append(add_group_obj)
                ag_dict = EnvelopedData.build_data_structures(add_group_obj_list)
                for k, v in ag_dict.items():
                    is_show = EnvelopedData.estimate_classify(v)
                    # is_show = 1 ---相当于管理员类，显示除了管理员组，级别以下的所有用户组
                    if is_show == 1:
                        # 重新判断新添加用户组的is_show，并判断是否展示
                        except_admin_groups_list = Groups.query.filter(Groups.id != 1).all()  # 教师、学生及新添加
                        add_groups_list = Groups.query.filter(Groups.id != 1, Groups.id != 2, Groups.id != 3).all()
                        child_ag_dict = EnvelopedData.build_data_structures(add_groups_list)
                        for k, v in child_ag_dict.items():
                            child_is_show = EnvelopedData.estimate_classify(v)
                            # 如果新添加用户组的is_show=1---相当于管理员类，则不显示，删除
                            if child_is_show == 1:
                                except_admin_groups_list.remove(
                                    Groups.query.filter(Groups.id == k).first())
                                continue
                            else:
                                # 不进行操作
                                continue
                        res_group_list = EnvelopedData.return_group_list(except_admin_groups_list)
                        return resp_hanlder(code=5001, msg='Display all user group information successfully.', result=res_group_list)

                    if is_show == 2:
                        except_teacher_groups_list = Groups.query.filter(Groups.id != 1, Groups.id != 2).all()  # 排除管理员、教师的用户组列表
                        add_groups_list = Groups.query.filter(Groups.id != 1, Groups.id != 2, Groups.id != 3).all()
                        child_ag_dict = EnvelopedData.build_data_structures(add_groups_list)
                        for k, v in child_ag_dict.items():
                            child_is_show = EnvelopedData.estimate_classify(v)
                            # 如果新添加用户组的is_show=1 或者 is_show=2---相当于管理员类或者教师组类，则不显示，删除
                            if child_is_show == 1 or child_is_show == 2:
                                except_teacher_groups_list.remove(
                                    Groups.query.filter(Groups.id == k).first())
                                continue
                            else:
                                # 不进行操作
                                continue
                        res_group_list = EnvelopedData.return_group_list(except_teacher_groups_list)
                        return resp_hanlder(code=5001, msg='Display all user group information successfully.',
                                            result=res_group_list)
                    else:
                        return resp_hanlder(code=999, msg='The permissions of the user group are displayed incorrectly. '
                                                          'Please contact the administrator to check.')

        except Exception as err:
            return resp_hanlder(code=999, msg=str(err))



@usergroup.route("/post/", methods=["POST", "PUT"], defaults={"desc": {"interface_name": "添加编辑用户组信息","is_permission": True,"permission_belong": 3}})
def post_group(desc):
    '''
     说明:添加编辑用户组接口
     参数:Authorization,dmp_group_id,dmp_group_name,creator,dmp_permission
          说明:用户标识信息token,dmp_group_name为用户组名,dmp_group_id为编辑的用户组id,dmp_permission为用户组对应的权限(列表),
          creator为创建者,若有creator参数则选择,没有creator则默认为当前登录的用户,数据类型:JSON
     返回值:成功返回状态码、对应提示信息及添加的用户组信息,数据类型:JSON,数据格式:{'msg':'...','results':{'x':'x'},'status':xxx}
     '''
    auth_token = request.headers.get('Authorization')
    res = PuttingData.get_obj_data(Users, auth_token)

    data = request.json
    dmp_group_id = data.get('dmp_group_id')
    dmp_group_name = data.get('dmp_group_name')
    creator = data.get('creator')
    dmp_permission_str = data.get('dmp_permission')
    dmp_permission_list = [int(p) for p in dmp_permission_str]

    # 添加用户组信息
    if request.method == 'POST' and dmp_group_id == None:
        try:
            group_obj = Groups(dmp_group_name=dmp_group_name)
            db.session.add(group_obj)
            db.session.commit()
            ret_data = EnvelopedData.post_edit(res, group_obj, creator, dmp_permission_list, dmp_group_name)
            return resp_hanlder(code=5005, msg=RET.alert_code[5005], result=ret_data)
        except Exception as err:
            db.session.rollback()
            return resp_hanlder(code=999, msg=str(err))

    # 编辑用户组信息
    elif request.method == 'PUT' and dmp_group_id != None:
        try:
            edit_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
            edit_group_obj.dmp_group_name = dmp_group_name
            ret_data = EnvelopedData.post_edit(res, edit_group_obj, creator, dmp_permission_list, dmp_group_name)
            return resp_hanlder(code=5004, msg=RET.alert_code[5004], result=ret_data)
        except Exception as err:
            db.session.rollback()
            return resp_hanlder(code=999, msg=str(err))
    return resp_hanlder(code=999)


@usergroup.route("/del/", methods=["DELETE"], defaults={"desc": {"interface_name": "删除用户组","is_permission": True,"permission_belong": 3}})
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
            # +
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            if not isinstance(res, dict):
                return resp_hanlder(code=999)
            data = request.json
            dmp_group_id = data.get('dmp_group_id')
            del_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
            # 没有设置级联删除，手动删除用户组关联的所有用户对象
            Users.query.filter(Users.dmp_group_id == dmp_group_id).delete()
            db.session.delete(del_group_obj)
            db.session.commit()
            return resp_hanlder(code=5007, msg=RET.alert_code[5007])
        except Exception as err:
            return resp_hanlder(code=999, msg=str(err))