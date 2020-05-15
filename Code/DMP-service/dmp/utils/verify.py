from flask import session, jsonify

from dmp.rbac.service.init_permission import INIT_PERMISSION
from dmp.utils.validation import ValidationEmail


class LoginVerify():
    """登录校验及用户信息保存"""

    @classmethod
    def __session_init(cls, user, remember_me):
        # 初始化用户对应用户组的权限
        INIT_PERMISSION.permission_init(user)

        # 保存用户信息到session中
        # user_dict = user.user_to_dict()
        # session['user'] = user_dict

        # 保存用户登录状态
        session['is_login'] = True
        session['remember_me'] = remember_me

    @classmethod
    def __login_verify(cls, user):
        if user == None:
            return  {
                    'status': -1,
                    'msg': 'User name or password entered wrong, please login again',
                    'results': {}
                }
        if user.confirmed == False:
            email = user.email
            ValidationEmail().reactivate_email(user, email)
            return {
                'status': -1,
                'msg': 'Login failed, mailbox not activated.'
                       'The email reactivation link has been sent, please wait a moment',
                'results': {}
            }
        return

    @classmethod
    def __email_verify(cls, user):
        if user == None:
            return {
                'status': -1,
                'msg': 'Mailbox or password entered wrong, please login again',
                'results': {}
            }
        if user.confirmed == False:
            email = user.email
            ValidationEmail().reactivate_email(user, email)
            return {
                'status': -1,
                'msg': 'Login failed, mailbox not activated.'
                       'The email reactivation link has been sent, please wait a moment',
                'results': {}
            }
        return

    @classmethod
    def login_username_verify_init(cls, user, remember_me):
        res = cls.__login_verify(user)
        if res:
            return res
        else:
            cls.__session_init(user, remember_me)
            return True

    @classmethod
    def login_email_verify_init(cls, user, remember_me):
        res = cls.__email_verify(user)
        if res:
            return res
        else:
            cls.__session_init(user, remember_me)
            return True


class UserVerify():

    @classmethod
    def judge_superuser(cls, user):
        if not user:
            return {
                'status': -1,
                'msg': 'Do not have a super administrator, '
                       'please contact the administrator to create a super administrator first',
                'results': {}
            }
        else:return