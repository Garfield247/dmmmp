import re

from flask import session, request

from dmp.config import config
from dmp.models import Users
from dmp.utils.response_hanlder import resp_hanlder
from dmp.utils.verify import UserVerify
from dmp.utils.put_data import PuttingData


def rbac_middleware():

    url_rule = str(request.path)
    print('vvv', url_rule)

    # 白名单
    for i in config['default'].WHITE_LIST:
        if re.match(i, url_rule):
            return

    # 登录状态的校验
    is_login = session.get('is_login')
    if not is_login:
        return resp_hanlder(code=999, msg="Not logged in, please log in first.")
    else:
        # 已经登录时，进行几项校验：1. token是否存在  2. token是否失效或者正确
        # 如果登录时，token不存在，返回201；如果token存在，验证通过，则继续向下进行校验；
        # 如果token验证没通过，则清空cookie里面的session，重新登陆
        try:
            auth_token = request.headers['Authorization']
        except Exception as err:
            return resp_hanlder(code=201, err=err)

        if auth_token:
            res = UserVerify.verify_token(auth_token)
            if res == True:
                pass

            # token失效
            else:
                session.clear()
                return resp_hanlder(code=201, msg=res)


    # 免认证的校验
    for i in config['default'].NO_PERMISSION_LIST:
        if re.match(i, url_rule):
            return

    # 管理员拥有所有权限
    res = PuttingData.get_obj_data(Users, auth_token)
    if isinstance(res, dict):
        if res.get('dmp_group_id') == 1:
            return
    else:
        return resp_hanlder(code=999, msg=res)

    # 权限校验
    permissions = session.get('SESSION_PERMISSION_URL')
    for i in permissions:
        if re.match(r'^{}$'.format(i['route']), url_rule):
            return
    print('The user does not have access rights')
    return resp_hanlder(code=301)

