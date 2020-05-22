from datetime import timedelta

from flask import session, jsonify, current_app, request

from dmp.rbac.service.init_permission import INIT_PERMISSION
from dmp.utils.validation import ValidationEmail
from dmp.models.dmp_user import Users


class LoginVerify():
    """登录校验及用户信息保存"""

    @classmethod
    def __session_init(cls, user):
        # 初始化用户对应用户组的权限
        INIT_PERMISSION.permission_init(user)
        # 保存用户登录状态
        session['is_login'] = True

        # 设置flask的session失效时间，这里保持了与token失效时间一致，保证关闭浏览器之后在打开仍可以访问
        # (因为flask的session在关闭浏览器之后失效)，
        session.permanent = True
        current_app.permanent_session_lifetime = timedelta(minutes=3600)

    @classmethod
    def __login_verify(cls, user):
        if user == None:
            return {
                'status': -1,
                'msg': 'Username is not registered or entered wrong, please login again',
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
    def login_username_verify_init(cls, user):
        res = cls.__login_verify(user)
        if res:
            return res
        else:
            if user.verify_password(request.json.get('password')):
                pass
            else:
                return {-1: 'Username or password error, please login again.'}
            cls.__session_init(user)
            return True

    @classmethod
    def login_email_verify_init(cls, user):
        res = cls.__email_verify(user)
        if res:
            return res
        else:
            if user.verify_password(request.json.get('password')):
                pass
            else:
                return {-1: 'Username or password error, please login again.'}
            cls.__session_init(user)
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
        else:
            return

    @classmethod
    def verify_token(cls, token):
        # 验证token的有效性
        res = Users.decode_auth_token(token)
        if not isinstance(res, str):
            return True
        else:
            return res
