#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

# from flask import session
#
#
# class INIT_PERMISSION(object):
#
#     @classmethod
#     def permission_init(cls, user_obj):
#         # permissions为Permission表对象的集合
#         permissions = user_obj.groups.permissions
#         # 当前角色对应的权限列表
#         permission_list = []
#
#         # 构建菜单字典
#         menu_dict = {}
#
#         for item in permissions:
#             permission_list.append({'route': item.route})
#             dmp_group_id = user_obj.dmp_group_id
#             if not dmp_group_id:
#                 continue
#             if dmp_group_id not in menu_dict:
#                 menu_dict[dmp_group_id] = {
#                     'children': [{
#                         'dmp_permission_name': item.dmp_permission_name,
#                         'route': item.route
#                     }]
#                 }
#             else:
#                 menu_dict[dmp_group_id]['children'].append({
#                     'dmp_permission_name': item.dmp_permission_name,
#                     'route': item.route
#                 })
#
#         """
#         permission_list = [{
#             'route': '/customer/list/'
#         }, {
#             'route': '/customer/add/'
#         }, {
#             'route': '/customer/edit/(?P<cid>\\d+)/'
#         }, {
#             'route': '/customer/del/(?P<cid>\\d+)/'
#         }, {
#             'route': '/payment/list/'
#         }]
#         ------------------------------------------------------
#         menu_dict = {
#             1: {
#                 'id': 1,
#                 'name': '用户管理',
#                 'parent': 1,
#                 {'children': [{
#                     'url': '/usergroup/info/',
#                     'name': '用户组管理'
#                     },{
#                     'url': '/user/list/',
#                     'name': '用户管理'
#                     }] }
#                 },
#             }
#
#         """
#         session['SESSION_PERMISSION_URL'] = permission_list
#         session['SESSION_MENU'] = menu_dict
#         print('999---', session.get('SESSION_PERMISSION_URL'))
#         print('888---', session.get('SESSION_MENU'))

        # 999--- [{'route': '/user/del/'}, {'route': '/user/list/'}, {'route': '/user/changeprofile/'},
        #         {'route': '/user/icon/'}, {'route': '/user/info/'}, {'route': '/user/changeprofile/'}, {'route': '/user/logout/'}]

        # 888--- {1: {'children': [{'dmp_permission_name': '删除用户', 'route': '/user/del/'}, {'dmp_permission_name': '用户列表', 'route': '/user/list/'},
        # {'dmp_permission_name': '修改资料', 'route': '/user/changeprofile/'}, {'dmp_permission_name': '头像上传', 'route': '/user/icon/'},
        # {'dmp_permission_name': '获取用户信息', 'route': '/user/info/'}, {'dmp_permission_name': '修改资料', 'route': '/user/changeprofile/'},
        # {'dmp_permission_name': '用户退出', 'route': '/user/logout/'}]}}
