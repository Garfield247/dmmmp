#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from dmp.models import Users, Groups
from dmp.utils.put_data import PuttingData


class INIT_PERMISSION(object):

    @classmethod
    def permission_init(cls, auth_token):

        # 当前角色对应的权限列表
        user_permissions_list = []

        res = PuttingData.get_obj_data(Users, auth_token)
        user_group_obj = Groups.query.filter(Groups.id == res.get('dmp_group_id')).first()
        user_permissions_obj_list = user_group_obj.permissions
        for p in user_permissions_obj_list:
            d = {}
            d['route'] = p.route
            user_permissions_list.append(d)
        return user_permissions_list

