#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD
import base64
import os

from flask import Blueprint, jsonify, request, session

from dmp.config import Config
from dmp.extensions import db
from dmp.models import Users, Groups
from dmp.rbac.middlewares.rbac import rbac_middleware
from dmp.rbac.service.init_permission import INIT_PERMISSION
from dmp.utils.validation import ValidationEmail

user = Blueprint("user", __name__, static_folder='Code/DMP-service/')


@user.route("/register/", methods=["POST"], defaults={"desc": "用户注册"})
def register(desc):
    try:
        user_obj = Users.query.all()
        if not user_obj:
            return jsonify({
                'status': -1,
                'msg': 'Do not have a super administrator, '
                       'please contact the administrator to create a super administrator first',
                'results': {}
            })
        dmp_username = request.form.get('dmp_username')
        real_name = request.form.get('real_name')
        passwd = request.form.get('password')
        email = request.form.get('email')
        user = Users(dmp_username=dmp_username, real_name=real_name, passwd=passwd, email=email,
                     leader_dmp_user_id=Config.LEADER_ROOT_ID)
        # 管理员单一添加用户-默认是学生用户组，直属管理者是root(1),邮箱已激活
        if session.get('is_login') and session.get('user').get('dmp_group_id') == 1:
            dmp_group_id = request.form.get('dmp_group_id')
            # 如果有所属组参数，则数据库跟新为所选所属组，如果没有参数，默认为3-students
            if dmp_group_id:
                user.dmp_group_id = dmp_group_id
            else:
                user.dmp_group_id = 3
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
            return jsonify({
                'status': 0,
                'msg': 'User single added successfully',
                'results': {}
            })
        db.session.add(user)
        db.session.commit()
        ValidationEmail().activate_email(user, email)
        result = {
            "status": 0,
            "msg": "The email has been sent. Please verify it",
            "results": 'OK'
        }
        return jsonify(result)
    except Exception:
        db.session.rollback()
        return jsonify({
            'status': -1,
            'msg': 'register error',
            'results': {}
        })


@user.route("/activate/", methods=["POST"], defaults={"desc": "用户激活"})
def activate(desc):
    pass


@user.route('/activate/<token>/', methods=['GET'])
def emailactivate(token):
    if Users.check_activate_token(token) == True:
        result = {
            "status": 0,
            "msg": "User activate successfully!",
            "results": {}
        }
        return jsonify(result)
    else:
        result = {
            "status": -1,
            "msg": "User activate failed!",
            "results": {}
        }
        return jsonify(result)


@user.route("/login/", methods=["POST"], defaults={"desc": "用户登录"})
def login(desc):
    dmp_username = request.form.get('dmp_username')
    email = request.form.get('email')
    passwd = request.form.get('password')
    remember_me = request.form.get('remember_me')
    if dmp_username and not email:
        user = Users.query.filter(Users.dmp_username == dmp_username, Users.passwd == passwd).first()
        if user == None:
            return jsonify({
                'status': -1,
                'msg': 'User name or password entered wrong, please login again',
                'results': {}
            })
        if user.confirmed == False:
            email = user.email
            ValidationEmail().reactivate_email(user, email)
            return jsonify({
                'status': -1,
                'msg': 'Login failed, mailbox not activated.'
                       'The email reactivation link has been sent, please wait a moment',
                'results': {}
            })
        INIT_PERMISSION.permission_init(user)
        user_dict = user.user_to_dict()
        session['user'] = user_dict
        session['is_login'] = True
        session['remember_me'] = remember_me
        return jsonify({
            'status': 0,
            'msg': 'Successful user login',
            'results': {}
        })
    elif email and not dmp_username:
        user = Users.query.filter(Users.email == email, Users.passwd == passwd).first()
        if user.confirmed == False:
            ValidationEmail().reactivate_email(user, email)
            return jsonify({
                'status': -1,
                'msg': 'Login failed, mailbox not activated.'
                       'The email reactivation link has been sent, please wait a moment',
                'results': {}
            })
        INIT_PERMISSION.permission_init(user)
        user_dict = user.user_to_dict()
        session['user'] = user_dict
        session['is_login'] = True
        session['remember_me'] = remember_me
        return jsonify({
            'status': 0,
            'msg': 'Successful user login',
            'results': {}
        })
    else:
        return jsonify({
            'status': -1,
            'msg': 'Login error',
            'results': {}
        })


@user.route("/logout/", methods=["GET"])
def logout():
    # 使用seesion控制登录、退出状态保存，可设置session的过期时间
    session.clear()
    return jsonify({
        'status': -1,
        'msg': 'User has logged out',
        'results': {}
    })


@user.route("/forgetpwd/", methods=["POST"], defaults={"desc": "找回密码"})
def forgetpwd(desc):
    email = request.form.get('email')
    user = Users.query.filter(Users.email == email).first()
    ValidationEmail().change_pwd(user, email)
    result = {
        "status": 0,
        "msg": "The password reset request has been sent to the mailbox. Please confirm the reset",
        "results": {}
    }
    return jsonify(result)


@user.route("/changepwd/", methods=["PUT"], defaults={"desc": "重设密码"})
def changepwd(desc):
    result = {
        "status": 0,
        "msg": "success",
        "results": {
        }
    }
    return jsonify(result)


@user.route('/gettoken/<token>', methods=['GET'])
def gettoken(token):
    return jsonify({
        'status': 0,
        'msg': 'Forget the password generated token',
        'results': token
    })


@user.route('/changepwd/', methods=['POST'])
def changepwd():
    token = request.form.get('token')
    newpassword = request.form.get('newpassword')
    success = Users.reset_password(token, newpassword)
    if success == True:
        return jsonify({
            'status': 0,
            'msg': 'Reset password successfully, please login again',
            'results': {}
        })
    else:
        return jsonify({
            'status': -1,
            'msg': 'Reset password failed, please try again',
            'results': {}
        })


# @user.route("/changepwd/<token>", methods=["GET"])
# def changepwd(token):
#     print('xxx', token)
#     new_password = request.form.get('newpassword')
#     success = Users.reset_password(token, new_password)
#     if success:
#         return jsonify({
#             'status': 0,
#             'msg': 'Reset password successfully, please login again',
#             'results': {}
#         })


@user.route("/list/", methods=["GET"], defaults={"desc": "用户列表"})
def ulist(desc):
    current_obj_dict = session['user']
    if current_obj_dict['dmp_group_id'] == 1:
        all_user_obj_list = Users.query.all()
        user_obj_dict_list = [u.user_to_dict() for u in all_user_obj_list]
        new_user_obj_dict_list = []
        for per_obj in user_obj_dict_list:
            dmp_group_obj = Groups.query.filter(Groups.id == per_obj['dmp_group_id']).first()
            if per_obj['leader_dmp_user_id'] == None:
                per_obj['leader_name'] = None
                dmp_group_name = dmp_group_obj.dmp_group_name
                group_permissions_list = dmp_group_obj.permissions
                p_list = []
                for p in group_permissions_list:
                    p_dict = {}
                    p_dict['id'] = p.id
                    p_dict['dmp_permission_name'] = p.dmp_permission_name
                    p_dict['route'] = p.route
                    p_list.append(p_dict)
                per_obj['dmp_group_name'] = dmp_group_name
                per_obj['u_group_permission'] = p_list
                new_user_obj_dict_list.append(per_obj)
                continue
            leader_obj_name = Users.query.filter(Users.id == per_obj['leader_dmp_user_id']).first().dmp_username
            dmp_group_name = dmp_group_obj.dmp_group_name
            group_permissions_list = dmp_group_obj.permissions
            p_list = []
            for p in group_permissions_list:
                p_dict = {}
                p_dict['id'] = p.id
                p_dict['dmp_permission_name'] = p.dmp_permission_name
                p_dict['route'] = p.route
                p_list.append(p_dict)

            per_obj['leader_name'] = leader_obj_name
            per_obj['dmp_group_name'] = dmp_group_name
            per_obj['u_group_permission'] = p_list
            new_user_obj_dict_list.append(per_obj)

        return jsonify({
            'status': 0,
            'msg': 'Display all user information',
            'results': new_user_obj_dict_list
        })
    # 管理员、教师登录，只需要显示用户的直属管理者是谁即可
    else:
        teacher_obj_dict = session.get('user')
        all_students_list = Users.query.filter(Users.leader_dmp_user_id == teacher_obj_dict['id']).all()
        stu_obj_dict_list = [u.user_to_dict() for u in all_students_list]
        new_stu_obj_dict_list = []
        for per_obj in stu_obj_dict_list:
            dmp_group_obj = Groups.query.filter(Groups.id == per_obj['dmp_group_id']).first()
            dmp_group_name = dmp_group_obj.dmp_group_name
            leader_obj_name = Users.query.filter(
                Users.leader_dmp_user_id == teacher_obj_dict['id']).first().dmp_username

            group_permissions_list = dmp_group_obj.permissions
            p_list = []
            for p in group_permissions_list:
                p_dict = {}
                p_dict['id'] = p.id
                p_dict['dmp_permission_name'] = p.dmp_permission_name
                p_dict['route'] = p.route
                p_list.append(p_dict)

            per_obj['leader_name'] = leader_obj_name
            per_obj['dmp_group_name'] = dmp_group_name
            per_obj['u_group_permission'] = p_list
            new_stu_obj_dict_list.append(per_obj)

        return jsonify({
            'status': 0,
            'msg': 'Display all user information',
            'results': new_stu_obj_dict_list
        })

        # dmp_group_name = Groups.query.filter(Groups.id == current_obj_dict['dmp_group_id']).first().dmp_group_name
        # u_group = current_obj.groups
        # u_group_permissions_list = u_group.permissions
        # l_list = []
        # for u in u_group_permissions_list:
        #     l_dict = {}
        #     l_dict['id'] = u.id
        #     l_dict['dmp_permission_name'] = u.dmp_permission_name
        #     l_dict['route'] = u.route
        #     l_list.append(l_dict)
        # current_obj_dict['dmp_group_name'] = dmp_group_name
        # current_obj_dict['u_group_permission'] = l_list
        # return jsonify({
        #     'status': 0,
        #     'msg': 'Display all user information',
        #     'results': current_obj_dict
        # })


@user.route("/info/", methods=["get"], defaults={"desc": "用户资料"})
def info(desc):
    # 默认返回当前用户信息，若传dmp_user_id参数，则返回指定id的用户信息
    # 返回json中包含当前用户的权限信息
    id = request.form.get('dmp_user_id')
    if not id:
        current_user_dict = session.get('user')
        current_obj = Users.query.filter(Users.id == current_user_dict['id']).first()
        dmp_group_name = Groups.query.filter(Groups.id == current_user_dict['dmp_group_id']).first().dmp_group_name
        u_group = current_obj.groups
        u_group_permissions_list = u_group.permissions
        u_list = []
        for p in u_group_permissions_list:
            p_dict = {}
            p_dict['id'] = p.id
            p_dict['dmp_permission_name'] = p.dmp_permission_name
            p_dict['route'] = p.route
            u_list.append(p_dict)
        current_user_dict['dmp_group_name'] = dmp_group_name
        current_user_dict['u_group_permission'] = u_list
        # 如果是管理员登录，则直属管理者只显示管理员
        if current_obj.dmp_group_id == 1:
            root_list_obj = Users.query.filter(Users.dmp_group_id == 1).all()
            r_list = []
            for u in root_list_obj:
                l_dict = {}
                l_dict['id'] = u.id
                l_dict['dmp_username'] = u.dmp_username
                r_list.append(l_dict)
            current_user_dict['leader_list'] = r_list
        else:
            # 教师及学生登录时，则展示所有管理员及教师--直属管理者
            from operator import or_
            user_obj_list = Users.query.filter(or_((Users.dmp_group_id == 1), (Users.dmp_group_id == 2))).all()
            l_list = []
            for u in user_obj_list:
                l_dict = {}
                l_dict['id'] = u.id
                l_dict['dmp_username'] = u.dmp_username
                l_list.append(l_dict)
            current_user_dict['leader_list'] = l_list
        return jsonify({
            'status': 0,
            'msg': 'Returns the current user object information by default',
            'results': current_user_dict
        })
    get_user_info_obj = Users.query.filter(Users.id == id).first()
    get_user_info_dict = get_user_info_obj.user_to_dict()
    u_group = get_user_info_obj.groups
    u_group_permissions_list = u_group.permissions
    u_list = []
    for p in u_group_permissions_list:
        p_dict = {}
        p_dict['id'] = p.id
        p_dict['dmp_permission_name'] = p.dmp_permission_name
        p_dict['route'] = p.route
        u_list.append(p_dict)
    get_user_info_dict['u_group_permission'] = u_list

    # 展示所有管理员及教师
    from operator import or_
    user_obj_list = Users.query.filter(or_((Users.dmp_group_id == 1), (Users.dmp_group_id == 2))).all()
    l_list = []
    for u in user_obj_list:
        l_dict = {}
        l_dict['id'] = u.id
        l_dict['dmp_username'] = u.dmp_username
        l_list.append(l_dict)
    get_user_info_dict['leader_list'] = l_list

    result = {
        'status': 0,
        'msg': 'Returns the object information by you choose',
        'results': get_user_info_dict
    }
    return jsonify(result)


@user.route("/icon/", methods=["POST"], defaults={"desc": "修改头像"})
def icon(desc):
    from dmp.utils.uuid_str import uuid_str
    current_obj_dict = session.get('user')
    current_obj = Users.query.filter(Users.id == current_obj_dict['id']).first()

    icon_obj_str = request.form.get('bin')
    icon_data = base64.b64decode(icon_obj_str)
    icon_name = uuid_str() + '.jpg'
    save_url = 'dmp/static/icon/'

    icon = open(save_url + icon_name, 'wb')
    icon.write(icon_data)
    icon.close()
    icon_obj = 'http://localhost:7789/static/icon/' + icon_name

    if os.path.exists(save_url + icon_name):
        origin_icon = current_obj.icon
        origin_icon_name = origin_icon.split('/')[-1]
        if origin_icon == None or origin_icon == '':
            pass
        elif origin_icon != None or origin_icon != '':
            os.remove(os.path.join(save_url, origin_icon_name))

    current_obj.icon = icon_obj
    db.session.add(current_obj)
    db.session.commit()

    icon_url = current_obj.user_to_dict()['icon']
    return jsonify({
        'status': 0,
        'msg': 'User profile photo uploaded successfully',
        'results': icon_url
    })


# 问题1：管理员单一添加默认的所属组是学生，直属管理者归为root1
# 添加所属组(相当于给用户分配权限)、直属管理者参数(默认不修改权限，修改权限到修改用户组那一栏修改)
@user.route("/changeprofile/", methods=["PUT"], defaults={"desc": "修改资料"})
def changeprofile(desc):
    dmp_user_id = request.form.get('dmp_user_id')
    # dmp_username = request.form.get('dmp_username')
    # real_name = request.form.get('real_name')
    passwd = request.form.get('password')
    email = request.form.get('email')
    confirmed = request.form.get('confirmed')

    dmp_group_id = request.form.get('dmp_group_id')
    leader_dmp_user_id = request.form.get('leader_dmp_user_id')

    if not dmp_user_id:
        try:
            current_user_dict = session.get('user')
            current_obj = Users.query.filter(Users.id == current_user_dict['id']).first()
            current_obj.email = email
            current_obj.passwd = passwd
            current_obj.dmp_group_id = dmp_group_id

            # 如果leader_dmp_user_id为空，表示的是超级管理员，不直属与任何一个用户
            if current_obj.leader_dmp_user_id == None:
                return jsonify({
                    'status': -1,
                    'msg': 'The super administrator is not directly affiliated with anyone',
                    'results': {}
                })

            # 当前用户的直属管理者 改为 选择对象的id  ---自关联
            choose_leader_obj = Users.query.filter(Users.id == leader_dmp_user_id).first()
            current_obj.leader_dmp_user_id = choose_leader_obj.id

            current_obj.leader_dmp_user_id = leader_dmp_user_id
            current_obj.confirmed = True if confirmed else False
            db.session.commit()
            # 构建返回数据:包括用户对应的用户组及用户组权限
            select_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
            select_obj_permissions_list = select_group_obj.permissions
            s_list = []
            for p in select_obj_permissions_list:
                p_dict = {}
                p_dict['id'] = p.id
                p_dict['dmp_permission_name'] = p.dmp_permission_name
                p_dict['route'] = p.route
                s_list.append(p_dict)

            ret_obj = Users.query.filter(Users.id == current_user_dict['id']).first()
            ret_obj_dict = ret_obj.user_to_dict()
            ret_obj_dict['group_permission'] = s_list

            return jsonify({
                'status': 0,
                'msg': 'The default user information has been changed',
                'results': ret_obj_dict
            })
        except:
            db.session.rollback()
            return jsonify({
                'status': -1,
                'msg': 'User information modification failed',
                'results': {}
            })
    try:
        choose_user_obj = Users.query.filter(Users.id == dmp_user_id).first()
        choose_user_obj_dict = choose_user_obj.user_to_dict()
        choose_user_obj.email = email
        choose_user_obj.passwd = passwd
        choose_user_obj.dmp_group_id = dmp_group_id
        # 构建返回数据:包括用户所属的直属管理者
        # 如果leader_dmp_user_id为空，表示的是超级管理员，不直属与任何一个用户
        if leader_dmp_user_id == None:
            return jsonify({
                'status': -1,
                'msg': 'The super administrator is not directly affiliated with anyone',
                'results': {}
            })

        choose_leader_obj = Users.query.filter(Users.id == leader_dmp_user_id).first()
        choose_user_obj.leader_dmp_user_id = choose_leader_obj.id

        choose_user_obj.leader_dmp_user_id = leader_dmp_user_id
        choose_user_obj.confirmed = True if confirmed else False
        db.session.commit()

        select_group_obj = Groups.query.filter(Groups.id == dmp_group_id).first()
        select_obj_permissions_list = select_group_obj.permissions
        s_list = []
        for p in select_obj_permissions_list:
            p_dict = {}
            p_dict['id'] = p.id
            p_dict['dmp_permission_name'] = p.dmp_permission_name
            p_dict['route'] = p.route
            s_list.append(p_dict)
        choose_user_obj_dict['group_permission'] = s_list

        ret_obj = Users.query.filter(Users.id == dmp_user_id).first()
        ret_obj_dict = ret_obj.user_to_dict()
        ret_obj_dict['group_permission'] = s_list

        result = {
            'status': 0,
            'msg': 'The currently selected user information has changed',
            'results': ret_obj_dict
        }
        return jsonify(result)
    except:
        db.session.rollback()
        return jsonify({
            'status': -1,
            'msg': 'User information modification failed',
            'results': {}
        })


@user.route("/frozen/", methods=["POST"])
def frozen_user():
    dmp_user_id = request.form.get('dmp_user_id')
    if not dmp_user_id:
        current_obj_dict = session.get('user')
        frozen_user_obj = Users.query.filter(Users.id == current_obj_dict['id'])
    else:
        frozen_user_obj = Users.query.filter(Users.id == dmp_user_id).first()
    if frozen_user_obj.dmp_group_id == 1 and frozen_user_obj.leader_dmp_user_id == None:
        return jsonify({
            'status': -1,
            'msg': 'The super administrator cannot freeze, please select another action',
            'results': {}
        })
    frozen_user_obj.confirmed = False
    db.session.commit()
    return jsonify({
        'status': 0,
        'msg': 'This user has been frozen. Please contact the administrator if you need to defrost',
        'results': {}
    })


@user.route("/del/", methods=["DELETE"], defaults={"desc": "删除用户"})
def udel(desc):
    dmp_user_id = request.form.get('dmp_user_id')
    # 超级管理员无法删除
    if dmp_user_id == "1":
        return jsonify({
            'status': -1,
            'msg': 'The super administrator could not delete',
            'results': {}
        })
    del_user_obj = Users.query.filter(Users.id == dmp_user_id).first()
    db.session.delete(del_user_obj)
    db.session.commit()
    return jsonify({
        'status': 0,
        'msg': 'User deletion successful',
        'results': {}
    })


@user.before_request
def before_request():
    rbac_middleware()
