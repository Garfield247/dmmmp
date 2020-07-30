#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

import base64
import os
import time

from flask import Blueprint, request, session, current_app
from operator import or_, and_

from dmp.extensions import db
from dmp.models import Users, Groups
from dmp.utils.rbac.middlewares import rbac_middleware
from dmp.utils.put_data import PuttingData
from dmp.utils.validation import ValidationEmail
from dmp.utils.verify import LoginVerify
from dmp.utils import resp_hanlder
from dmp.utils.response_hanlder import RET
from dmp.utils.verify import UserVerify
from dmp.utils.uuid_str import uuid_str
from dmp.utils.ep_data import EnvelopedData

user = Blueprint("user", __name__, static_folder='Code/DMP-service/')


@user.route("/register/", methods=["POST"], defaults={"desc": {"interface_name": "用户注册", "is_permission": False, "permission_belong": None}})
def register(desc):
    '''
    说明:用户注册及超级管理员单一添加用户接口
    参数:dmp_username,real_name,password,email;说明:客户端请求参数信息,数据类型:JSON
    返回值:成功与失败返回对应的状态码及提示信息,数据类型:JSON,数据格式:{'msg':'...','results':null,'status':xxx}
    '''
    try:
        user_obj = Users.query.filter_by(id=1).first()
        # 判断初始状态有没有超级用管理员，没有则不能创建用户，必须要先创建一个超级管理员
        ret = UserVerify.judge_superuser(user_obj)
        if ret:
            return resp_hanlder(code=999, msg=ret)
        data = request.json
        if data == None:
            return resp_hanlder(code=999)
        auth_token = data.get('Authorization')
        dmp_username = data.get('dmp_username')
        real_name = data.get('real_name')
        passwd = data.get('password')
        email = data.get('email')
        user = Users(dmp_username=dmp_username, real_name=real_name, password=passwd,
                     email=email, leader_dmp_user_id=1)
        res_token = PuttingData.get_obj_data(Users, auth_token)
        if auth_token != None and isinstance(res_token, dict):
            res = PuttingData.root_add_user(data, res_token, user, dmp_username, real_name)
            # 返回字典-管理员单一添加成功
            if isinstance(res, dict):
                return resp_hanlder(code=0, msg=res)

            # 返回元组-管理员/教师单一添加缺少参数
            elif isinstance(res, tuple):
                return resp_hanlder(code=999, msg=res[1])

            # 普通管理员和教师无法添加管理员角色，需要超级管理员添加
            elif res == False:
                return resp_hanlder(code=999, msg='Could not add an administrator user.')
        # 返回token错误的字符串-注册成功(注册时无token)
        db.session.add(user)
        db.session.commit()
        ValidationEmail().activate_email(user, email)
        return resp_hanlder(code=1001, msg=RET.alert_code[1001])
    except Exception as err:
        db.session.rollback()
        return resp_hanlder(code=999, msg=str(err))


@user.route("/activate/", methods=["POST"], defaults={"desc": {"interface_name": "用户激活", "is_permission": False, "permission_belong": None}})
def activate(desc):
    '''
    说明:用户邮箱激活接口
    参数:Authorization,说明:邮件生成的客户端标识,通过json传入,数据类型:JSON
    返回值:成功返回状态码及对应提示信息,数据类型:JSON,数据格式:{'msg':'...','results':null,'status':xxx}
    '''
    try:
        # 激活邮箱--注册时激活、token失效或者忘记导致未激活
        token = request.json.get('Authorization')
        res = PuttingData.get_obj_data(Users, token)
        # 校验token的有效期及正确性
        if isinstance(res, dict):
            if res.get('confirmed') == True:
                return resp_hanlder(code=999, msg=RET.alert_code[1014])
            # 已激活,confirmed为True
            if Users.check_activate_token(res) == True:
                return resp_hanlder(code=1009, msg=RET.alert_code[1009])
        else:
            return resp_hanlder(code=2002, msg=RET.alert_code[2002])
    except Exception as err:
        return resp_hanlder(code=999, msg=str(err))


@user.route("/login/", methods=["POST"], defaults={"desc": {"interface_name": "用户登录", "is_permission": False, "permission_belong": None}})
def login(desc):
    '''
    说明:用户登陆接口
    参数:Authorization,dmp_username,email,password,说明:用户可选择用户名或邮箱登录,数据类型:JSON
    返回值:成功返回状态码、对应提示信息和客户端标识token,数据类型:JSON,数据格式:{'msg':'...','results':'xxx.sss.ccc','status':1003}
    '''
    if request.method == 'POST':
        try:
            data = request.json
            email = data.get('email')
            dmp_username = data.get('dmp_username')
            if dmp_username and not email:
                user = Users.query.filter(Users.dmp_username == dmp_username).first()
                r = LoginVerify.login_username_verify_init(user)
                if r == True:
                    auth_token = user.encode_auth_token()
                    if auth_token:
                        # session['auth_token'] = auth_token.decode('utf-8')
                        return resp_hanlder(code=1003, msg=RET.alert_code[1003], result=auth_token.decode('utf-8'))
                    return resp_hanlder(code=201)
                else:
                    return resp_hanlder(code=999, msg=r[-1])

            elif email and not dmp_username:
                user = Users.query.filter(Users.email == email).first()
                r = LoginVerify.login_email_verify_init(user)
                if r == True:
                    auth_token = user.encode_auth_token()
                    if auth_token:
                        # session['auth_token'] = auth_token.decode('utf-8')
                        return resp_hanlder(code=1003, msg=RET.alert_code[1003], result=auth_token.decode('utf-8'))
                    return resp_hanlder(code=201)
                else:
                    return resp_hanlder(code=999, msg=r[-1])
            else:
                return resp_hanlder(code=999)
        except Exception as err:
            return resp_hanlder(code=1004, msg=RET.alert_code[1004], err=err)


@user.route("/forgetpwd/", methods=["POST"], defaults={"desc": {"interface_name": "找回密码", "is_permission": False, "permission_belong": None}})
def forgetpwd(desc):
    '''
     说明:用户找回密码接口
     参数:email,说明:用户忘记密码的邮箱，数据类型:JSON
     返回值:成功返回状态码及对应提示信息,数据类型:JSON,数据格式:{'msg':'...','results':null,'status':xxx}
     '''
    if request.method == 'POST':
        try:
            data = request.json
            email = data.get('email')
            user = Users.query.filter(Users.email == email).first()
            ValidationEmail().change_pwd(user, email)
            return resp_hanlder(code=1002, msg=RET.alert_code[1002])
        except Exception as err:
            return resp_hanlder(code=999, msg=str(err))


@user.route('/changepwd/', methods=['PUT'], defaults={"desc": {"interface_name": "重设密码", "is_permission": False, "permission_belong": None}})
def changepwd(desc):
    '''
     说明:用户重设密码接口
     参数:Authorization,newpassword,说明:重置密码生成的标识token及新密码,都通过json传入，数据类型:JSON
     返回值:成功返回状态码及对应提示信息,数据类型:JSON,数据格式:{'msg':'...','results':null,'status':xxx}
     '''
    if request.method == 'PUT':
        try:
            data = request.json
            token = data.get('authorization')
            newpassword = data.get('newpassword')
            res = Users.reset_password(token, newpassword)
            if res == True:
                return resp_hanlder(code=1006, msg=RET.alert_code[1006])
            else:
                return resp_hanlder(code=1007, msg=res)
        except Exception as err:
            return resp_hanlder(code=999, msg=str(err))


@user.route("/list/", methods=["GET"], defaults={"desc": {"interface_name": "用户列表", "is_permission": True, "permission_belong": 1}})
def ulist(desc):
    '''
     说明:获取用户列表接口,管理员显示所有用户,教师显示直属管理者是自己的用户
     参数:Authorization,说明:用户登录标识token，数据类型:String
     返回值:成功返回状态码、对应提示信息及用户列表,数据类型:JSON,数据格式:{'msg':'...','results':[{'x':'x'},..'],'status':xxx}
     '''
    if request.method == 'GET':
        # 获取用户列表
        try:
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            # 超级管理员显示所有的用户
            if res.get('id') == 1:
                all_user_obj_list = Users.query.filter(Users.is_deleted == 0).all()
                new_user_obj_dict_list = EnvelopedData.ulist(all_user_obj_list, res=None)
                return resp_hanlder(code=3001, msg=RET.alert_code[3001], result=new_user_obj_dict_list)
            # 普通管理员只显示管理员级别以下的所有用户(teacher/student或者一些属于新添加用户组的用户等)，
            # 即只拥有用户管理或用户组管理(理论上，实际不可能单独拥有用户组管理权限)之一的权限
            if res.get('dmp_group_id') == 1 and res.get('id') != 1:
                # 新添加用户组的所有用户对象
                add_user_obj = Users.query.filter(
                                    Users.dmp_group_id != 1,
                                    Users.dmp_group_id != 2,
                                    Users.dmp_group_id != 3).all()
                user_dict = EnvelopedData.build_data_structures_ulist(add_user_obj)
                show_user_list = []
                for k, v in user_dict.items():
                    is_show = EnvelopedData.estimate_classify(v)
                    # 新添加的用户组 没有同时 拥有用户管理和用户组管理权限，则普通管理员显示
                    if is_show != 1:
                        add_show_user_obj = Users.query.filter(Users.id == k, Users.is_deleted == 0).first()
                        if add_show_user_obj:
                            show_user_list.append(add_show_user_obj)
                        else:
                            continue
                # 普通管理员默认只展示教师和学生，不展示新添加的用户组用户，需要判断才能决定是否展示
                all_user_obj_list = Users.query.filter(
                    Users.is_deleted == 0,
                    or_((Users.dmp_group_id == 2), (Users.dmp_group_id == 3))).all()
                # 将默认初始化的可以展示的用户和新添加判断后可以展示的用户 相加
                all_user_obj_list = all_user_obj_list + show_user_list
                new_user_obj_dict_list = EnvelopedData.ulist(all_user_obj_list, res=None)

                return resp_hanlder(code=3001, msg=RET.alert_code[3001], result=new_user_obj_dict_list)
            # 教师登录，只显示直属管理者是自己的学生,且排除逻辑删除的学生
            # else:
            if res.get('dmp_group_id') == 2:
                # 新添加用户组的所有用户对象
                add_user_obj = Users.query.filter(
                                    Users.dmp_group_id != 1,
                                    Users.dmp_group_id != 2,
                                    Users.dmp_group_id != 3).all()
                user_dict = EnvelopedData.build_data_structures_ulist(add_user_obj)
                show_child_user_list = []
                for k, v in user_dict.items():
                    is_show = EnvelopedData.estimate_classify(v)
                    # 新添加的用户组 同时没有 拥有用户管理和用户组管理权限，则教师显示
                    # 相当于is_show==3,先判断是属于学生用户组类别
                    if is_show != 1 and is_show != 2 and is_show != 4:
                        add_show_user_obj = Users.query.filter(Users.id == k, Users.is_deleted == 0).first()
                        if add_show_user_obj.leader_dmp_user_id == res.get('id'):
                            show_child_user_list.append(add_show_user_obj)
                        else:
                            continue
                # 教师默认只展示直属领导的学生，不展示新添加的用户组用户，需要判断同时没有那两种权限才能展示
                # all_students_list = Users.query.filter(and_((Users.leader_dmp_user_id == res['id']), (Users.is_deleted == 0))).all()
                # 筛选默认用户组中：剔除逻辑删除用户、学生属于当前老师的
                all_students_list = Users.query.filter(
                    and_(Users.dmp_group_id > 0, Users.dmp_group_id < 4),
                    Users.leader_dmp_user_id == res['id'],
                    Users.is_deleted == 0).all()
                all_students_list = all_students_list + show_child_user_list
                new_stu_obj_dict_list = EnvelopedData.ulist(all_students_list, res)
                return resp_hanlder(code=3001, msg=RET.alert_code[3001], result=new_stu_obj_dict_list)
            # 属于新添加的用户组用户登录
            else:
                # 针对新添加的用户组
                # 用户属于新添加的用户组，拿到用户对应的新用户组--对应的新用户组权限--判断权限中有无/user/list/,/usergroup/info/权限
                # 判断is_show的值，如果为1，则相当于管理员，如果为2，则相当于教师，如果为3，则相当于学生，没权限访问ulist接口
                new_obj = Users.query.filter(Users.id == res.get('id')).first()
                new_group = new_obj.groups
                new_permission_list = new_group.permissions
                l = []
                for p in new_permission_list:
                    l.append({'route': p.route})
                is_show = EnvelopedData.estimate_classify(l)
                # 相当于普通管理员，能够看到普通管理员用户组级别以下的所有用户信息(过滤掉管理员、及同级别的新用户组用户)
                if is_show == 1:
                    all_user_obj_list = Users.query.filter(
                        Users.is_deleted == 0,
                        Users.dmp_group_id != 1,
                        Users.dmp_group_id != res.get('dmp_group_id')).all()
                    new_user_obj_dict_list = EnvelopedData.ulist(all_user_obj_list, res=None)
                    g = EnvelopedData.glist(new_user_obj_dict_list)
                    # 进行新添用户组的is_show判断
                    for u in g:
                        u_p = u.get('u_group_permission')
                        is_show = EnvelopedData.estimate_classify(u_p)
                        # 判断新添加的用户组的is_show，如果新添加的用户组is_show等于1，相当于管理员权限，不显示，删掉
                        if is_show == 1:
                            new_user_obj_dict_list.remove(u)
                    return resp_hanlder(code=3001, msg=RET.alert_code[3001], result=new_user_obj_dict_list)
                # 相当于教师，能够看到教师用户组级别以下的所有用户组信息，用户组只有/user/list/及其他，没有/usergroup/info/
                # 将管理员用户组、教师用户组及同级别的新用户组的用户信息过滤掉,
                # 还得判断新添加其他的用户组的is_show,is_show=3才能给教师权限类别 显示
                if is_show == 2:
                    all_user_list = Users.query.filter(
                        Users.is_deleted == 0,
                        Users.dmp_group_id != 1,
                        Users.dmp_group_id != 2,
                        Users.dmp_group_id != res.get('dmp_group_id')).all()
                    new_user_obj_dict_list = EnvelopedData.ulist(all_user_list, res)
                    g = EnvelopedData.glist(new_user_obj_dict_list)
                    for u in g:
                        u_p = u.get('u_group_permission')
                        is_show = EnvelopedData.estimate_classify(u_p)
                        # 判断新添加的用户组的is_show，如果is_show等于1或2，相对于教师权限来说就不显示，删掉
                        if is_show == 1 or is_show == 2:
                            new_user_obj_dict_list.remove(u)
                    return resp_hanlder(code=3001, msg=RET.alert_code[3001], result=new_user_obj_dict_list)
                # 下面两个条件无法进入
                if is_show == 3:
                    # 没有权限进入此路由
                    return resp_hanlder(code=999, msg='You do not have permission to access this route, '
                                                      'or the permissions are incorrectly assigned, '
                                                      'please contact the administrator')
                if is_show == 4:
                    return resp_hanlder(code=999, msg='There is a problem with user rights allocation, '
                                                      'please contact the administrator to resolve it')
                else:
                    return resp_hanlder(code=999, msg='There is a problem with user rights allocation, '
                                                      'please contact the administrator to resolve it')

        except Exception as err:
            return resp_hanlder(code=999, msg=str(err))


@user.route("/info/", methods=["GET"], defaults={"desc": {"interface_name": "用户资料", "is_permission": True, "permission_belong": 0}})
def info(desc):
    '''
     说明:获取用户资料接口
     参数:Authorization,dmp_user_id,说明:没有dmp_user_id默认返回当前用户信息,有dmp_user_id返回指定id的用户信息，数据类型:JSON
     返回值:成功返回状态码、对应提示信息及用户资料信息,数据类型:JSON,数据格式:{'msg':'...','results':{'x':'x'},'status':xxx}
     '''
    if request.method == 'GET':
        # 默认返回当前用户信息，若传dmp_user_id参数，则返回指定id的用户信息
        # 返回json中包含当前用户的权限信息
        try:
            data = request.json
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            # 没有dmp_user_id:表示当前用户信息
            if data == None:
                # 当前用户
                current_obj = Users.query.filter(Users.id == res['id']).first()
                dmp_group_name = Groups.query.filter(Groups.id == res['dmp_group_id']).first().dmp_group_name
                # 当前用户所对应的用户组
                u_group = current_obj.groups
                ret = EnvelopedData.info_s2_data(u_group, res, dmp_group_name)

                # 教师及管理员登录时，则展示所有管理员及教师--直属管理者
                user_obj_list = Users.query.filter(or_((Users.dmp_group_id == 1), (Users.dmp_group_id == 2))).all()
                new_res = EnvelopedData.info_s1_data(user_obj_list, ret)
                return resp_hanlder(code=3002, msg=RET.alert_code[3002], result=new_res)

            dmp_user_id = data.get('dmp_user_id')
            get_user_info_obj = Users.query.filter(Users.id == dmp_user_id).first()
            get_user_info_dict = get_user_info_obj.__json__()
            u_group = get_user_info_obj.groups
            dmp_group_name = Groups.query.filter(Groups.id == get_user_info_dict['dmp_group_id']).first().dmp_group_name
            ret = EnvelopedData.info_s2_data(u_group, get_user_info_dict, dmp_group_name)

            # 展示所有管理员及教师
            user_obj_list = Users.query.filter(or_((Users.dmp_group_id == 1), (Users.dmp_group_id == 2))).all()
            new_ret = EnvelopedData.info_s1_data(user_obj_list, ret)
            return resp_hanlder(code=3003, msg=RET.alert_code[3003], result=new_ret)

        except Exception as err:
            return resp_hanlder(code=999, msg=str(err))


@user.route("/icon/", methods=["POST"], defaults={"desc": {"interface_name": "修改头像", "is_permission": False, "permission_belong": None}})
def icon(desc):
    '''
     说明:修改用户头像接口
     参数:Authorization,说明:修改指定用户的头像信息，数据类型:JSON
     返回值:成功返回状态码、对应提示信息及头像地址,数据类型:JSON,数据格式:{'msg':'...','results':'http://...','status':xxx}
     '''
    if request.method == 'POST':
        try:
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            data = request.json
            if data == None:
                return resp_hanlder(code=999)
            icon_obj_str = data.get('bin')
            icon_obj_str = icon_obj_str.split(',')[-1]
            current_obj = Users.query.filter(Users.id == res['id']).first()
            icon_data = base64.b64decode(icon_obj_str)
            icon_name = uuid_str() + '.jpg'
            save_url = current_app.config.get("SAVE_URL")
            origin_icon = current_obj.icon
            if origin_icon:
                origin_icon_path = os.path.join(save_url, origin_icon)
                if os.path.exists(origin_icon_path):
                    os.remove(origin_icon_path)
            new_icon_path = os.path.join(save_url, icon_name)
            with open(new_icon_path, 'wb') as new_icon:
                new_icon.write(icon_data)
            current_obj.icon = current_app.config.get("ICON_URL") + icon_name
            current_obj.put()
            icon_url = current_obj.icon
            return resp_hanlder(code=4001, msg=RET.alert_code[4001], result=icon_url)
        except Exception as err:
            db.session.rollback()
            return resp_hanlder(code=999, msg=str(err))


@user.route("/changeprofile/", methods=["PUT"], defaults={"desc": {"interface_name": "修改资料", "is_permission": True, "permission_belong": 0}})
def changeprofile(desc):
    '''
     说明:修改用户资料接口
     参数:Authorization,dmp_user_id,password,email,confirmed,dmp_group_id,leader_dmp_user_id,
          说明:指定用户标识token,没有dmp_user_id默认修改当前用户信息,有dmp_user_id修改指定id的用户信息，email为用户邮箱,
          confirmed为用户状态是否激活,dmp_group_id为用户所属组,leader_dmp_user_id为用户所属直属领导者,数据类型:JSON
     返回值:成功返回状态码、对应提示信息及修改后的用户资料信息,数据类型:JSON,数据格式:{'msg':'...','results':{'x':'x'},'status':xxx}
     '''
    if request.method == 'PUT':
        # + try
        try:
            # 修改信息-不允许修改权限信息(与用户组关联),展示的时候默认阴影，不能勾选；要是想修改权限，只能修改用户组权限
            data = request.json
            if data == None:
                return resp_hanlder(code=999)
            dmp_user_id = data.get('dmp_user_id')
            passwd = data.get('password')
            email = data.get('email')
            confirmed = data.get('confirmed')
            dmp_group_id = data.get('dmp_group_id')
            leader_dmp_user_id = data.get('leader_dmp_user_id')
            dmp_username = data.get('dmp_username')
            real_name = data.get('real_name')
            dmp_user_info = data.get('dmp_user_info')
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            current_obj = Users.query.filter(Users.id == res['id']).first()

            if not dmp_user_id:
                # 管理员、教师、学生--只修改dmp_username、real_name、password和email四个字段信息
                # 修改邮箱时，发送邮件进行验证
                if confirmed == None and dmp_group_id == None and leader_dmp_user_id == None:
                    # 单独修改用户简介的信息
                    if dmp_user_info != None and not dmp_username and not real_name and not passwd and not email:
                        current_obj.dmp_user_info = dmp_user_info
                        db.session.commit()
                        return resp_hanlder(code=1015, msg=RET.alert_code[1015])
                    # 单独修改密码的信息
                    elif passwd and not dmp_username and not real_name and not email and not dmp_user_info:
                        current_obj.password = passwd
                        db.session.commit()
                        return resp_hanlder(code=1015, msg=RET.alert_code[1015])
                    # 获取当前登录用户信息(同时修改4个参数信息-新邮箱需要重新发送邮箱校验)，并进行修改--root、teacher、student都可
                    else:
                        ret = EnvelopedData.edit_private_info(current_obj, email, passwd, dmp_username, real_name)
                        if isinstance(ret, str):
                            return resp_hanlder(code=0, msg=ret)
                        else:
                            return resp_hanlder(code=999, msg=ret[1])
                EnvelopedData.changeprofile(current_obj, email, passwd, dmp_group_id,
                                            confirmed, leader_dmp_user_id, dmp_username, real_name)
                # 构建返回数据:包括用户对应的用户组及用户组权限
                select_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
                ret_obj = Users.query.filter(Users.id == res['id']).first()
                ret_obj_dict = ret_obj.user_to_dict()
                ret_obj_dict = EnvelopedData.p_changeprofile(select_group_obj, ret_obj_dict)
                return resp_hanlder(code=3004, msg=RET.alert_code[3004], result=ret_obj_dict)
            choose_user_obj = Users.query.filter(Users.id == dmp_user_id).first()
            choose_user_obj_dict = choose_user_obj.user_to_dict()
            EnvelopedData.changeprofile(choose_user_obj, email, passwd, dmp_group_id,
                                        confirmed, leader_dmp_user_id, dmp_username, real_name)
            select_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
            choose_user_obj_dict = EnvelopedData.p_changeprofile(select_group_obj, choose_user_obj_dict)
            return resp_hanlder(code=3006, msg=RET.alert_code[3006], result=choose_user_obj_dict)

        except Exception as err:
            db.session.rollback()
            return resp_hanlder(code=999, msg=str(err))


@user.route("/frozen/", methods=["POST"], defaults={"desc": {"interface_name": "冻结用户", "is_permission": True, "permission_belong": 1}})
def frozen_user(desc):
    '''
     说明:冻结用户接口
     参数:Authorization,dmp_user_id,说明:指定用户标识token,没有dmp_user_id默认指定冻结自己,有dmp_user_id冻结指定id的用户,将confirmed改为false,数据类型:JSON
     返回值:成功返回状态码及对应提示信息,数据类型:JSON,数据格式:{'msg':'...','results':null,'status':xxx}
     '''
    if request.method == 'POST':
        data = request.json
        auth_token = request.headers.get('Authorization')
        res = PuttingData.get_obj_data(Users, auth_token)
        try:
            # 没有dmp_user_id，默认冻结自己
            if data == None:
                frozen_user_obj = Users.query.filter(Users.id == res['id']).first()
            else:
                dmp_user_id = data.get('dmp_user_id')
                frozen_user_obj = Users.query.filter(Users.id == dmp_user_id).first()
            # 超级管理员不可以冻结
            if frozen_user_obj.id == 1:
                return resp_hanlder(code=4003, msg=RET.alert_code[4003])
            frozen_user_obj.confirmed = False
            db.session.commit()
            return resp_hanlder(code=4004, msg=RET.alert_code[4004])
        except Exception as err:
            return resp_hanlder(code=999, msg=str(err))


@user.route("/del/", methods=["DELETE"], defaults={"desc": {"interface_name": "删除用户", "is_permission": True, "permission_belong": 1}})
def udel(desc):
    '''
    说明:删除用户接口
    参数:Authorization,dmp_user_id,说明:指定用户标识token,超级管理员无法删除,根据dmp_user_id删除指定的用户信息,数据类型:JSON
    返回值:成功返回状态码及对应提示信息,数据类型:JSON,数据格式:{'msg':'...','results':null,'status':xxx}
    '''
    if request.method == 'DELETE':
        try:
            # +
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            if not isinstance(res, dict):
                return resp_hanlder(code=999)
            data = request.json
            if data == None:
                return resp_hanlder(code=999)
            dmp_user_id = data.get('dmp_user_id')
            del_user_obj = Users.query.filter(Users.id == dmp_user_id).first()
            # 超级管理员无法删除
            if del_user_obj.id == 1:
                return resp_hanlder(code=4005, msg=RET.alert_code[4005])
            else:
                # 逻辑删除，并改变用户名(加了时间戳)
                del_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                del_time = del_time.split(' ')[0] + "-" + del_time.split(' ')[1]
                if '[' and ']' not in del_user_obj.dmp_username:
                    del_user_obj.is_deleted = True
                    del_user_obj.dmp_username = del_user_obj.dmp_username + '[DELETED ON:' + del_time + ']'
                    del_user_obj.email = del_user_obj.email + '[DELETED ON:' + del_time + ']'
                    db.session.commit()
                else:
                    dn = del_user_obj.dmp_username.split('[')[0]
                    del_user_obj.dmp_username = dn + '[' + del_time + ']'
                    db.session.commit()
                return resp_hanlder(code=4006, msg=RET.alert_code[4006])
        except Exception as err:
            return resp_hanlder(code=999, msg=str(err))


@user.before_request
def before_request():
    '''
    说明:钩子函数-权限校验以及token传入是否正确及有效性校验
    参数:无
    返回值:有权限访问url通过,没权限访问返回提示信息,数据类型:JSON,数据格式:{'msg':'...','results':null,'status':301}
    '''
    rbac_middleware()
