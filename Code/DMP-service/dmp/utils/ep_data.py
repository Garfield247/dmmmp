from operator import or_

from flask import session

from dmp.extensions import db
from dmp.models import Groups, Users, Permissions


class EnvelopedData():

    @staticmethod
    def __ulist_same_data(dmp_group_obj, per_obj, dict_list, leader_obj_name):
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
        dict_list.append(per_obj)
        return dict_list

    @staticmethod
    def info_s1_data(list_obj, res):
        lr_list = []
        for u in list_obj:
            l_dict = {}
            l_dict['id'] = u.id
            l_dict['dmp_username'] = u.dmp_username
            lr_list.append(l_dict)
        res['leader_list'] = lr_list
        return res

    @staticmethod
    def info_s2_data(u_group, ret_obj_dict, dmp_group_name):
        # 封装了用户组对应的权限
        u_group_permissions_list = u_group.permissions
        u_list = []
        for p in u_group_permissions_list:
            p_dict = {}
            p_dict['id'] = p.id
            p_dict['dmp_permission_name'] = p.dmp_permission_name
            p_dict['route'] = p.route
            u_list.append(p_dict)

        ret_obj = Users.query.filter(Users.id == ret_obj_dict['id']).first()
        new_ret_obj_dict = ret_obj.user_to_dict()
        new_ret_obj_dict['dmp_group_name'] = dmp_group_name
        new_ret_obj_dict['group_permission'] = u_list
        return new_ret_obj_dict

    @staticmethod
    def __user_profile(current_obj, email, passwd, dmp_group_id, confirmed):
        current_obj.email = email
        current_obj.password = passwd
        current_obj.dmp_group_id = dmp_group_id
        current_obj.confirmed = True if confirmed else False
        return

    @classmethod
    def ulist(cls, all_obj_list, res):
        obj_dict_list = [u.__json__() for u in all_obj_list]
        new_obj_dict_list = []
        for per_obj in obj_dict_list:
            dmp_group_obj = Groups.query.filter(Groups.id == per_obj['dmp_group_id']).first()
            if per_obj['leader_dmp_user_id'] == None:
                per_obj['leader_name'] = None
                cls.__ulist_same_data(dmp_group_obj, per_obj, new_obj_dict_list, leader_obj_name=None)
                continue
            else:
                if res == None:
                    leader_obj_name = Users.query.filter(Users.id == per_obj['leader_dmp_user_id']).first().dmp_username
                    # cls.__ulist_same_data(dmp_group_obj, per_obj, new_obj_dict_list, leader_obj_name)
                else:
                    leader_obj_name = Users.query.filter(Users.id == res['id']).first().dmp_username
                cls.__ulist_same_data(dmp_group_obj, per_obj, new_obj_dict_list, leader_obj_name)
        return new_obj_dict_list

    @classmethod
    def changeprofile(cls, current_obj, email, passwd, dmp_group_id, confirmed, leader_dmp_user_id):
        cls.__user_profile(current_obj, email, passwd, dmp_group_id, confirmed)

        # 如果leader_dmp_user_id为空，表示的是超级管理员，不直属与任何一个用户
        if current_obj.leader_dmp_user_id == None:
            current_obj.leader_dmp_user_id = None
        else:
            choose_leader_obj = Users.query.filter(Users.id == leader_dmp_user_id).first()
            current_obj.leader_dmp_user_id = choose_leader_obj.id
            current_obj.leader_dmp_user_id = leader_dmp_user_id
        db.session.commit()
        return

    @classmethod
    def p_changeprofile(cls, u_group, ret_obj_dict):
        dmp_group_name = Groups.query.filter(Groups.id == ret_obj_dict['dmp_group_id']).first().dmp_group_name
        new_ret_obj_dict = cls.info_s2_data(u_group, ret_obj_dict, dmp_group_name)
        return new_ret_obj_dict

    @classmethod
    def usergroup_info(cls, groups_all):
        groups_list = []
        for per_group_obj in groups_all:
            groups_list.append(per_group_obj)
        res_group_list = [g.__json__() for g in groups_list]
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
        return res_group_list, d

    @classmethod
    def grouplist(cls, permission_list, current_group_obj):
        p_list = []
        for p in permission_list:
            if len(permission_list) == 0:
                break
            p_list.append(p.permission_to_dict())
        current_group_obj_dict = current_group_obj.group_to_dict()
        creator = session.get('creator')
        current_group_obj_dict['group_permission'] = p_list
        current_group_obj_dict['creator'] = creator
        return current_group_obj_dict

    @classmethod
    def post_edit(cls, res, group_obj, creator, dmp_permission_list, dmp_group_name):
        ret_data = group_obj.group_to_dict()
        if creator:
            ret_data['creator'] = creator
        else:
            creator = res.get('dmp_username')
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
        return ret_data

    @classmethod
    def total_users(cls):
        teachers_list = Users.query.filter(Users.dmp_group_id == 2).all()
        students_list = Users.query.filter(Users.dmp_group_id == 3).all()
        teachers_max_count = Groups.query.filter(Groups.id == 2).first().max_count
        students_max_count = Groups.query.filter(Groups.id == 3).first().max_count
        if len(teachers_list) >= teachers_max_count:
            return 'The number of teachers exceeds the maximum capacity of the teacher group. Please operate again'
        if len(students_list) >= students_max_count:
            return 'The number of students exceeds the maximum capacity of the student group. Please operate again'
        else:
            return True
