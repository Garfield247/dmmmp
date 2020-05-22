#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD
import base64
import os
from operator import or_

from flask import Blueprint, jsonify, request, session

from dmp.config import Config, config
from dmp.extensions import db
from dmp.models import Users, Groups
from dmp.rbac.middlewares.rbac import rbac_middleware
from dmp.utils.put_data import PuttingData
from dmp.utils.validation import ValidationEmail
from dmp.utils.verify import LoginVerify
from dmp.utils import resp_hanlder
from dmp.utils.response_hanlder import RET
from dmp.utils.verify import UserVerify
from dmp.utils.uuid_str import uuid_str
from dmp.utils.ep_data import EnvelopedData

user = Blueprint("user", __name__, static_folder='Code/DMP-service/')


@user.route("/register/", methods=["POST"], defaults={"desc": "用户注册"})
def register(desc):
    try:
        user_obj = Users.query.all()
        # 判断初始状态有没有超级用管理员，没有则不能创建用户，必须要先创建一个超级管理员
        res = UserVerify.judge_superuser(user_obj)
        if res:
            return jsonify(res)
        data = request.json
        dmp_username = data.get('dmp_username')
        real_name = data.get('real_name')
        passwd = data.get('password')
        email = data.get('email')
        user = Users(dmp_username=dmp_username, real_name=real_name, password=passwd,
                     email=email, leader_dmp_user_id=Config.LEADER_ROOT_ID)
        res = PuttingData.root_add_user(user)

        # 返回字典-管理员单一添加成功
        if isinstance(res, dict):
            return resp_hanlder(code=0, msg=res)
        # 返回元组-超出用户组最大容量
        elif isinstance(res, tuple):
            return resp_hanlder(code=999, msg=res[1])

        db.session.add(user)
        db.session.commit()
        ValidationEmail().activate_email(user, email)
        return resp_hanlder(code=1001, msg=RET.alert_code[1001])
    except Exception as err:
        db.session.rollback()
        return resp_hanlder(code=101, err=err)


@user.route("/activate/<token>", methods=["GET"], defaults={"desc": "用户激活"})
def activate(token, desc):
    # 激活邮箱--注册时激活、token失效或者忘记导致未激活
    res = PuttingData.get_obj_data(Users, token)
    if Users.check_activate_token(res) == True:
        return resp_hanlder(code=1009, msg=RET.alert_code[1009])
    else:
        return resp_hanlder(code=2002, msg=RET.alert_code[2002])


@user.route("/login/", methods=["POST"], defaults={"desc": "用户登录"})
def login(desc):
    if request.method == 'POST':
        try:
            data = request.json
            dmp_username = data.get('dmp_username')
            email = data.get('email')
            # passwd = data.get('password')
            if dmp_username and not email:
                user = Users.query.filter(Users.dmp_username == dmp_username).first()
                r = LoginVerify.login_username_verify_init(user)
                if r == True:
                    auth_token = user.encode_auth_token()
                    if auth_token:
                        return resp_hanlder(code=1003, msg=RET.alert_code[1003], result=auth_token.decode('utf-8'))
                    return resp_hanlder(code=201)
                else:
                    return resp_hanlder(code=999, msg=r)

            elif email and not dmp_username:
                user = Users.query.filter(Users.email == email).first()
                r = LoginVerify.login_email_verify_init(user)
                if r == True:
                    auth_token = user.encode_auth_token()
                    return resp_hanlder(code=1003, msg=RET.alert_code[1003], result=auth_token.decode('utf-8'))
                else:
                    return jsonify(r)
            return resp_hanlder(code=999)
        except Exception as err:
            return resp_hanlder(code=1004, msg=RET.alert_code[1004], err=err)


@user.route("/logout/", methods=["GET"], defaults={"desc": "用户退出"})
def logout(desc):
    if request.method == 'GET':
        # 清空session中所有保存的信息
        session.clear()
        return resp_hanlder(code=1005, msg=RET.alert_code[1005])


@user.route("/forgetpwd/", methods=["POST"], defaults={"desc": "找回密码"})
def forgetpwd(desc):
    if request.method == 'POST':
        try:
            data = request.json
            email = data.get('email')
            user = Users.query.filter(Users.email == email).first()
            ValidationEmail().change_pwd(user, email)
            return resp_hanlder(code=1002, msg=RET.alert_code[1002])
        except Exception as err:
            return resp_hanlder(code=999, err=err)


@user.route('/gettoken/<token>', methods=['GET'])
def gettoken(token):
    return jsonify({
        'status': 0,
        'msg': 'Forget the password generated token',
        'results': token
    })


@user.route('/changepwd/', methods=['POST'], defaults={"desc": "重设密码"})
def changepwd(desc):
    if request.method == 'POST':
        data = request.json
        token = request.headers.get('Authorization')
        newpassword = data.get('newpassword')
        res = Users.reset_password(token, newpassword)
        if res == True:
            session.clear()
            return resp_hanlder(code=1006, msg=RET.alert_code[1006])
        else:
            return resp_hanlder(code=1007, msg=res)


@user.route("/list/", methods=["GET"], defaults={"desc": "用户列表"})
def ulist(desc):
    if request.method == 'GET':
        # 获取用户列表
        try:
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            if res.get('dmp_group_id') == 1:
                all_user_obj_list = Users.query.all()
                new_user_obj_dict_list = EnvelopedData.ulist(all_user_obj_list, res=None)
                return resp_hanlder(code=3001, msg=RET.alert_code[3001], result=new_user_obj_dict_list)
            # 管理员、教师登录，只需要显示用户的直属管理者是谁即可
            else:
                all_students_list = Users.query.filter(Users.leader_dmp_user_id == res['id']).all()
                new_stu_obj_dict_list = EnvelopedData.ulist(all_students_list, res)
                return resp_hanlder(code=3001, msg=RET.alert_code[3001], result=new_stu_obj_dict_list)
        except Exception as err:
            return resp_hanlder(code=999, err=err)


@user.route("/info/", methods=["GET"], defaults={"desc": "用户资料"})
def info(desc):
    if request.method == 'GET':
        # 默认返回当前用户信息，若传dmp_user_id参数，则返回指定id的用户信息
        # 返回json中包含当前用户的权限信息
        try:
            data = request.json
            dmp_user_id = data.get('dmp_user_id')
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            # 没有dmp_user_id:表示当前用户信息
            if not dmp_user_id:
                current_obj = Users.query.filter(Users.id == res['id']).first()
                dmp_group_name = Groups.query.filter(Groups.id == res['dmp_group_id']).first().dmp_group_name
                u_group = current_obj.groups
                ret = EnvelopedData.info_s2_data(u_group, res, dmp_group_name)

                # 如果是管理员登录，则直属管理者只显示管理员
                if current_obj.dmp_group_id == 1:
                    root_list_obj = Users.query.filter(Users.dmp_group_id == 1).all()
                    new_res = EnvelopedData.info_s1_data(root_list_obj, ret)
                else:
                    # 教师及学生登录时，则展示所有管理员及教师--直属管理者
                    user_obj_list = Users.query.filter(or_((Users.dmp_group_id == 1), (Users.dmp_group_id == 2))).all()
                    new_res = EnvelopedData.info_s1_data(user_obj_list, ret)
                return resp_hanlder(code=3002, msg=RET.alert_code[3002], result=new_res)

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
            return resp_hanlder(code=999, err=err)


@user.route("/icon/", methods=["POST"], defaults={"desc": "修改头像"})
def icon(desc):
    if request.method == 'POST':
        try:
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            data = request.json
            icon_obj_str = data.get('bin')
            current_obj = Users.query.filter(Users.id == res['id']).first()
            icon_data = base64.b64decode(icon_obj_str)
            icon_name = uuid_str() + '.jpg'
            save_url = config['default'].SAVE_URL
            icon = open(save_url + icon_name, 'wb')
            icon.write(icon_data)
            icon.close()
            icon_obj = os.path.join(config['default'].ICON_URL, icon_name)
            if os.path.exists(save_url + icon_name):
                origin_icon = current_obj.icon
                if origin_icon == None or origin_icon == '':
                    pass
                elif origin_icon != None or origin_icon != '':
                    # 在linux下路径分隔符需要改变
                    origin_icon_name = origin_icon.split('/')[-1]
                    os.remove(os.path.join(save_url, origin_icon_name))
            current_obj.icon = icon_obj
            db.session.add(current_obj)
            db.session.commit()
            icon_url = current_obj.__json__().get('icon')
            return resp_hanlder(code=4001, msg=RET.alert_code[4001], result=icon_url)
        except Exception as err:
            db.session.rollback()
            return resp_hanlder(code=999, err=err)


@user.route("/changeprofile/", methods=["PUT"], defaults={"desc": "修改资料"})
def changeprofile(desc):
    if request.method == 'PUT':
        # 修改信息-不允许修改权限信息(与用户组关联),展示的时候默认阴影，不能勾选；要是想修改权限，只能修改用户组权限
        dmp_user_id = request.form.get('dmp_user_id')
        passwd = request.form.get('password')
        email = request.form.get('email')
        confirmed = request.form.get('confirmed')
        dmp_group_id = request.form.get('dmp_group_id')
        leader_dmp_user_id = request.form.get('leader_dmp_user_id')
        auth_token = request.headers.get('Authorization')
        res = PuttingData.get_obj_data(Users, auth_token)
        if not dmp_user_id:
            try:
                current_obj = Users.query.filter(Users.id == res['id']).first()
                EnvelopedData.changeprofile(current_obj, email, passwd, dmp_group_id,
                                            confirmed, leader_dmp_user_id)
                # 构建返回数据:包括用户对应的用户组及用户组权限
                select_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
                ret_obj = Users.query.filter(Users.id == res['id']).first()
                ret_obj_dict = ret_obj.__json__()
                ret_obj_dict = EnvelopedData.p_changeprofile(select_group_obj, ret_obj_dict)

                return resp_hanlder(code=3004, msg=RET.alert_code[3004], result=ret_obj_dict)
            except:
                db.session.rollback()
                return resp_hanlder(code=3005, msg=RET.alert_code[3005])
        try:
            choose_user_obj = Users.query.filter(Users.id == dmp_user_id).first()
            choose_user_obj_dict = choose_user_obj.__json__()
            EnvelopedData.changeprofile(choose_user_obj, email, passwd, dmp_group_id, confirmed, leader_dmp_user_id)
            select_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
            choose_user_obj_dict = EnvelopedData.p_changeprofile(select_group_obj, choose_user_obj_dict)

            return resp_hanlder(code=3006, msg=RET.alert_code[3006], result=choose_user_obj_dict)
        except Exception as err:
            db.session.rollback()
            return resp_hanlder(code=3005, msg=RET.alert_code[3005], err=err)


@user.route("/frozen/", methods=["POST"], defaults={"desc": "冻结用户"})
def frozen_user():
    if request.method == 'POST':
        data = request.json
        dmp_user_id = data.get('dmp_user_id')

        auth_token = request.headers.get('Authorization')
        res = PuttingData.get_obj_data(Users, auth_token)
        try:
            # 没有dmp_user_id，默认冻结自己
            if not dmp_user_id:
                frozen_user_obj = Users.query.filter(Users.id == res['id'])
            else:
                frozen_user_obj = Users.query.filter(Users.id == dmp_user_id).first()
            # 超级管理员不可以冻结
            if frozen_user_obj.dmp_group_id == 1 and frozen_user_obj.leader_dmp_user_id == None:
                return resp_hanlder(code=4003, msg=RET.alert_code[4003])
            frozen_user_obj.confirmed = False
            db.session.commit()
            return resp_hanlder(code=4004, msg=RET.alert_code[4004])
        except Exception as err:
            return resp_hanlder(code=999, err=err)


@user.route("/del/", methods=["DELETE"], defaults={"desc": "删除用户"})
def udel(desc):
    if request.method == 'DELETE':
        dmp_user_id = request.form.get('dmp_user_id')
        del_user_obj = Users.query.filter(Users.id == dmp_user_id).first()
        # 超级管理员无法删除
        if del_user_obj.dmp_group_id == 1 and del_user_obj.leader_dmp_user_id == None:
            return resp_hanlder(code=4005, msg=RET.alert_code[4005])
        # 删除管理员-用户组列表的管理员数量减一
        elif del_user_obj.dmp_group_id == 1 and del_user_obj.leader_dmp_user_id != None:
            root_obj_group = Groups.query.filter(Groups.id == del_user_obj.dmp_group_id).first()
            root_obj_group.max_count -= 1
            db.session.delete(del_user_obj)
            db.session.commit()
        else:
            db.session.delete(del_user_obj)
            db.session.commit()
            return resp_hanlder(code=4006, msg=RET.alert_code[4006])


@user.before_request
def before_request():
    rbac_middleware()
