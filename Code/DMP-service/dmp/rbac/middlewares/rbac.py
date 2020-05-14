import re

from flask import session, request, jsonify

from dmp.config import config


def rbac_middleware():
    url_rule = str(request.path)
    print('vvv', url_rule)
    for i in config['default'].WHITE_LIST:
        if re.match(i, url_rule):
            return

    # 登录状态的校验
    is_login = session.get('is_login')
    if not is_login:
        result = {
            'stauts': -1,
            'msg': 'Not logged in, please log in first',
            'result': {}
        }
        return jsonify(result)

    # 免认证的校验
    for i in config['default'].NO_PERMISSION_LIST:
        if re.match(i, url_rule):
            return

    user_dict = session.get('user')
    dmp_group_id = user_dict.get('dmp_group_id')
    if dmp_group_id == 1:
        return

    # 权限校验
    permissions = session.get('SESSION_PERMISSION_URL')
    for i in permissions:
        if re.match(r'^{}$'.format(i['route']), url_rule):
            return
    print('The user does not have access rights')
    return jsonify({
        'status': 301,
        'msg': 'You do not have access to this route. Please contact your administrator',
        'result': {}
    })
