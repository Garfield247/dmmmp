#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

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
            return 'Registration failed, please check the relevant reason (username or mailbox may have been used).'

    @classmethod
    def __add_info(cls, res_token, user, dmp_group_name, dmp_username, real_name):
        # 用户名和真实姓名必填
        if dmp_group_name and len(dmp_username) != 0 and len(real_name) != 0:
            dmp_group_obj = Groups.query.filter(Groups.dmp_group_name == dmp_group_name).first()
            if dmp_group_obj == None:
                return False
            user.dmp_group_id = dmp_group_obj.id
            user.confirmed = True
            user.leader_dmp_user_id = res_token.get('id')
            cls.__add_commit(user)
            return True
        else:
            return False

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
    def root_add_user(cls, data, res_token, user, dmp_username, real_name):
        # dmp_group_id = data.get('dmp_group_id')
        dmp_group_name = data.get('dmp_group_name')
        if not isinstance(res_token, str):
            # 只有是超级管理员才能进行单一添加root、teacher及student
            # 用户名及邮箱已经通过接口验证-唯一性
            if res_token.get('id') == 1:
                r = cls.__add_info(res_token, user, dmp_group_name, dmp_username, real_name)
                if r == True:
                    # 返回字典表示单一添加成功
                    return {True: 'Super admin user single added successfully.'}
                else:
                    return (-1, 'Missing parameter or incorrect user group name.')

            # 管理员单一添加teacher及student
            # 普通管理员无法单一添加管理员角色,需要超级管理员添加管理员角色
            if res_token.get('dmp_group_id') == 1 and res_token.get('id') != 1:
                dmp_group_obj = Groups.query.filter(Groups.dmp_group_name == dmp_group_name).first()
                if dmp_group_obj == None:
                    return (-1, 'Missing parameter or incorrect user group name.')
                dmp_group_id = dmp_group_obj.id
                if dmp_group_id == 1:
                    return -1
                else:
                    r = cls.__add_info(res_token, user, dmp_group_name, dmp_username, real_name)
                    if r == True:
                        return {True: 'Admin user single added successfully.'}
                    else:
                        return (-1, 'Missing parameter or incorrect user group name.')

            # 教师可以单一添加教师
            if res_token.get('dmp_group_id') == 2:
                dmp_group_obj = Groups.query.filter(Groups.dmp_group_name == dmp_group_name).first()
                if dmp_group_obj == None:
                    return (-1, 'Missing parameter or incorrect user group name.')
                dmp_group_id = dmp_group_obj.id
                if dmp_group_id == 1 or dmp_group_id == 2:
                    return -2
                else:
                    r = cls.__add_info(res_token, user, dmp_group_name, dmp_username, real_name)
                    if r == True:
                        return {True: 'Teacher user single added successfully.'}
                    else:
                        return (-1, 'Missing parameter or incorrect user group name.')
        # 返回报错token字符串
        return res_token
