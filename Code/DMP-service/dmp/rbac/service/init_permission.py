from flask import session
from dmp.models import Permissions


class INIT_PERMISSION(object):

    @classmethod
    def permission_init(cls, user_obj):

        # permissions为Permission表对象的集合
        permissions = user_obj.groups.permissions

        # 当前角色对应的权限列表
        permission_list = []

        # 当前橘色所构建的菜单字典
        menu_dict = {}

        for item in permissions:
            permission_list.append({'route': item.route})
            dmp_group_id = user_obj.dmp_group_id
            if not dmp_group_id:
                continue
            if dmp_group_id not in menu_dict:
                menu_dict[dmp_group_id] = {
                    'children': [{
                        'dmp_permission_name': item.dmp_permission_name,
                        'route': item.route
                    }]
                }
            else:
                menu_dict[dmp_group_id]['children'].append({
                    'dmp_permission_name': item.dmp_permission_name,
                    'route': item.route
                })
        print(permission_list)
        # [{'route': '/user/list/'}, {'route': '/usergroup/info/'}]
        print(menu_dict)
        # {1: {'children': [{'dmp_permission_name': '用户管理', 'route': '/user/list/'},
        #                   {'dmp_permission_name': '用户组管理 ', 'route': '/usergroup/info/'}]}}

        """
        permission_list = [{
            'route': '/customer/list/'
        }, {
            'route': '/customer/add/'
        }, {
            'route': '/customer/edit/(?P<cid>\\d+)/'
        }, {
            'route': '/customer/del/(?P<cid>\\d+)/'
        }, {
            'route': '/payment/list/'
        }]
        ------------------------------------------------------
        menu_dict = {
            1: {
                'id': 1,
                'name': '用户管理',
                'parent': 1,
                {'children': [{
                    'url': '/usergroup/info/',
                    'name': '用户组管理'
                    },{
                    'url': '/user/list/',
                    'name': '用户管理'
                    }] }
                },
            }
            
        """
        session['SESSION_PERMISSION_URL'] = permission_list
        session['SESSION_MENU'] = menu_dict
