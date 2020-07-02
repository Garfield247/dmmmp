#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

import re

from flask import request

from dmp.config import Config
from dmp.models import Users
from dmp.utils.response_hanlder import resp_hanlder
from dmp.utils.verify import UserVerify
from dmp.utils.put_data import PuttingData
from dmp.rbac.service.init_permission import INIT_PERMISSION


def rbac_middleware():
    url_rule = str(request.path)
    print('url_rule:', url_rule)

    # 白名单
    for i in Config.WHITE_LIST:
        if re.match(i, url_rule):
            return

    # 登录状态的校验
    # 验证有没有token，有继续执行，没有报错
    try:
        auth_token = request.headers['Authorization']
    except Exception as err:
        return resp_hanlder(code=201, err=err)

    # 有token，验证其有效性
    if auth_token:
        res = UserVerify.verify_token(auth_token)
        if res == True:
            pass
        # token失效或token验证失败,重新登陆
        else:
            return resp_hanlder(code=201, msg=res)

    # 免认证的校验
    for i in Config.NO_PERMISSION_LIST:
        if re.match(i, url_rule):
            return

    # 管理员拥有所有权限
    try:
        res = PuttingData.get_obj_data(Users, auth_token)
        if isinstance(res, dict):
            if res.get('dmp_group_id') == 1:
                return
        else:
            return resp_hanlder(code=999, msg=res)
    except Exception as err:
        return resp_hanlder(code=999, err=err)

    # 权限校验
    permissions = INIT_PERMISSION.permission_init(auth_token)
    for i in permissions:
        if re.match(r'^{}$'.format(i['route']), url_rule):
            return
    print('The user does not have access rights')
    return resp_hanlder(code=301)
