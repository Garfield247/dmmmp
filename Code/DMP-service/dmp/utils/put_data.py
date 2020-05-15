from flask import session, request

from dmp.extensions import db
from dmp.models import Users


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

    @staticmethod
    def get_obj_data(Model, token):
        resp = Model.decode_auth_token(token)
        if not isinstance(resp, str):
            user_obj = Users.query.filter_by(id=resp).first()
            # print('ooss', user_obj.__json__(), type(user_obj.__json__()))
            user_obj_dict = user_obj.__json__()
            return user_obj_dict
        else:
            return False


    @classmethod
    def put_data(cls, rootgroup, obj):

        if rootgroup.max_count == None:
            rootgroup.max_count = 1
        else:
            rootgroup.max_count += 1
        cls.__add_commit(obj)

    @classmethod
    def root_add_user(cls, user):

        # 管理员单一添加用户-默认是学生用户组，直属管理者是root(1),邮箱已激活
        if session.get('is_login') and session.get('user').get('dmp_group_id') == 1:
            dmp_group_id = request.form.get('dmp_group_id')
            # 如果有所属组参数，则数据库跟新为所选所属组，如果没有参数，默认为3-students
            if dmp_group_id:
                user.dmp_group_id = dmp_group_id
            else:
                user.dmp_group_id = 3
            user.confirmed = True
            cls.__add_commit(user)
            return {
                'status': 0,
                'msg': 'User single added successfully',
                'results': {}
            }
        return