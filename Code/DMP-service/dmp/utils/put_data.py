#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import session, request

from dmp.extensions import db
from dmp.models import Users, Groups


class PuttingData():

    @classmethod
    def __commit(cls):
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

    @classmethod
    def __add_commit(cls, obj):
        try:
            db.session.add(obj)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return 'Registration failed, please check the relevant reason (username or mailbox may have been used)'

    @staticmethod
    def get_obj_data(Model, token):
        resp = Model.decode_auth_token(token)
        if not isinstance(resp, str):
            # 获取对象-字典
            user_obj = Users.query.filter_by(id=resp).first()
            user_obj_dict = user_obj.__json__()
            return user_obj_dict
        # token失效或者错误
        else:
            return resp

    @classmethod
    def put_data(cls, rootgroup, obj):
        if rootgroup.max_count == None:
            rootgroup.max_count = 1
        else:
            rootgroup.max_count += 1
        ret = cls.__add_commit(obj)
        return ret

    @classmethod
    def root_add_user(cls, user):

        from dmp.utils.response_hanlder import resp_hanlder
        from dmp.utils.verify import UserVerify


        # 注册用户时-默认dmp_group_id=3，判断学生用户数量与数据库中学生用户组最大容量的关系
        ret = UserVerify.judge_count(user.dmp_group_id)
        # 返回tuple表示超出学生用户组最大容量
        if isinstance(ret, tuple):
            return ret

        # 管理员单一添加用户-默认是学生用户组，直属管理者是root(1),邮箱已激活
        # 没有Authorization参数，返回None
        auth_token = request.headers.get('Authorization')
        res = PuttingData.get_obj_data(Users, auth_token)
        data = request.json
        if data == None:
            return resp_hanlder(code=999)
        if not isinstance(res, str):
            # 只有是超级管理员才能进行单一添加root、teacher及student
            if res.get('id') == 1:
                dmp_group_id = data.get('dmp_group_id')
                ret = UserVerify.judge_count(dmp_group_id)
                if ret == True:
                    user.dmp_group_id = dmp_group_id
                    user.confirmed = True
                    cls.__add_commit(user)
                    return {True: 'Super admin user single added successfully'}
                else:
                    # 返回tuple，超出容量
                    return ret
            # 管理员单一添加teacher及student
            # 普通管理员无法单一添加管理员角色,需要超级管理员添加管理员角色
            if res.get('dmp_group_id') == 1 and res.get('id') != 1:
                dmp_group_id = data.get('dmp_group_id')
                if dmp_group_id == 1:
                    return False
                else:
                    ret = UserVerify.judge_count(dmp_group_id)
                    if ret == True:
                        user.dmp_group_id = dmp_group_id
                        user.confirmed = True
                        cls.__add_commit(user)
                        return {True: 'Admin user single added successfully'}
                    else:
                        # 返回tuple，超出容量
                        return ret
        # 返回报错token字符串
        return res
