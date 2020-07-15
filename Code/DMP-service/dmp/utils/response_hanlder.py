#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD 

from flask import jsonify


class RET():
    alert_code = {
        0: "success",
        # 参数类错误
        # 101: "required_parameter_missing",
        101: "required_parameter_error",
        # 权限类错误
        201: "Invalid_Token",
        301: "Permission_Denied",
        # 对象类错误
        404: "Item_Does_Not_Exist",
        # 数据库类错误
        501: "Connection_Failed",
        502: "Database_In_Use",
        # 其他错误
        999: "Other_Error",

        1001: "The email has been sent. Please verify it.",  # 邮件已发送，请激活
        1002: "The password reset request has been sent to the mailbox. Please confirm the reset.",  # 重置密码邮件已发送，请确认重置
        1003: "Successful user login.",  # 用户登陆成功
        1004: "Login error.",  # 登录错误
        1005: "User has logged out.",  # 用户已经退出
        1006: "Reset password successfully, please login again.",  # 重置密码成功，请重新登录
        1007: "Reset password failed, please try again.",  # 重置密码失败，请重新尝试
        1008: "The activated account does not exist.",  # 激活的账户不存在
        1009: "User activate successfully.",  # 用户激活成功
        1010: "Mailbox has been used, you should change the mailbox.",  # 邮箱已被使用，请更换邮箱
        1011: "Mailbox can be used, you can use it.",  # 邮箱可以使用，你可以使用
        1012: "Username has been used, please change the username.",  # 用户名已被使用，请重新更换用户名
        1013: "Username can be used, you can use it.",  # 用户名可以使用，你可以使用
        1014: "The mailbox has been activated. Please do not reactivate it.",  # 邮箱已激活，请勿重新激活
        1015: "User profile modified successfully.",
        1016: "Groupname has been used, please change the username.",
        1017: "Groupname can be used, you can use it.",

        2001: "Please provide a login token.",  # 请提供登录的token
        2002: "Token error, user activate failed.",  # token错误，用户激活失败
        3001: "Display all user information.",  # 展示所有的用户信息
        3002: "Returns the current user object information by default.",  # 返回当前默认的用户对象信息
        3003: "Returns information about the specified user.",  # 返回指定用户的信息
        3004: "The default user information has been changed.",  # 默认的用户信息已被修改
        3005: "User information modification failed.",  # 用户信息修改失败
        3006: "The currently selected user information has changed.",  # 当前选择的用户信息已被修改

        4001: "User profile icon uploaded successfully.",  # 用户头像上传成功
        4002: "The super administrator is not directly affiliated with anyone.",  # 超级管理员不直属于任何人
        4003: "The super administrator cannot freeze, please select another action.",  # 超级管理员不能被冻结，请选择其他操作
        4004: "This user has been frozen. Please contact the administrator if you need to defrost.",
        # 用户已被冻结，如果想要解冻，请联系管理员
        4005: "The super administrator could not delete.",  # 超级管理员无法删除
        4006: "User deletion successful.",  # 用户删除成功
        4007: "Root deletion successful.",  # 管理员删除成功

        5001: "Gets user group information and its corresponding permission information.",  # 获取用户组信息及对应的权限信息
        5002: "The user group information to be edited.",  # 获取需要被修改的用户组信息
        5003: "The maximum capacity of the administrator user group cannot be modified.",  # 管理员用户组最大容量不能被修改
        5004: "User group edited successfully.",  # 用户组修改成功
        # 5005: "User group name is unique, please select again",
        5005: "User group and corresponding permissions were added successfully.",  # 用户组及对应的权限添加成功
        5006: "User group name is unique, please select again.",  # 用户组名称不可重复，请重新选择
        5007: "Group deletion successful.",  # 用户组删除成功

        6001: "Returned all the permissions list."  # 返回所有的权限列表信息

    }


def resp_hanlder(**option):
    msg = option.get("msg")
    result = option.get("result")
    err = option.get("err")
    code = 999 if err and not option.get("code") else option.get("code", 0)
    if msg:
        response_body = {
            "status": code,
            "msg": str(err) or msg,
            "results": result
        }
    else:
        response_body = {
            "status": code,
            "msg": str(err) or RET.alert_code.get(code),
            "results": result
        }
    return jsonify(response_body)
