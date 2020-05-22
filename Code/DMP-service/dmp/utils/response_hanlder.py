#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD 

from flask import jsonify


class RET():
    response_code = {
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
        502: "Database_Occupied",
        # 其他错误
        999: "Other_Error",
    }

    alert_code = {
        1001: "The email has been sent. Please verify it",
        1002: "The password reset request has been sent to the mailbox. Please confirm the reset",
        1003: "Successful user login",
        1004: "Login error",
        1005: "User has logged out",
        1006: "Reset password successfully, please login again",
        1007: "Reset password failed, please try again",
        1008: "The activated account does not exist",  # 激活的账户不存在
        1009: "User activate successfully",  # 用户激活成功
        1010: "Mailbox has been used, you should change the mailbox",
        1011: "Mailbox can be used, you can use it",
        1012: "Username has been used, you should change the username",
        1013: "Username can be used, you can use it",
        2001: "Please provide a login token",
        2002: "Token error, user activate failed",  # token错误，用户激活失败
        3001: "Display all user information",
        3002: "Returns the current user object information by default",
        3003: "Returns information about the specified user",
        3004: "The default user information has been changed",
        3005: "User information modification failed",
        3006: "The currently selected user information has changed",
        4001: "User profile icon uploaded successfully",
        4002: "The super administrator is not directly affiliated with anyone",
        4003: "The super administrator cannot freeze, please select another action",
        4004: "This user has been frozen. Please contact the administrator if you need to defrost",
        4005: "The super administrator could not delete",
        4006: "User deletion successful",
        5001: "Gets user group information and its corresponding permission information",
        5002: "User group information to be edited",
        5003: "The maximum capacity of the administrator user group cannot be modified",
        5004: "User group edited successfully",
        # 5005: "User group name is unique, please select again",
        5005: "User group and corresponding permissions were added successfully",
        5006: "User group name is unique, please select again",
        5007: "Group deletion successful",
        6001: "Returned all the permissions list"

    }


def resp_hanlder(**option):
    msg = option.get("msg")
    result = option.get("result")
    err = option.get("err")
    code = 999 if err and not option.get("code") else option.get("code", 0)
    if msg:
        response_body = {
            "status": code,
            "msg": msg,
            "results": result if not err else {"error_msg": str(err)}
        }
    else:
        response_body = {
            "status": code,
            "msg": RET.response_code.get(code),
            "results": result if not err else {"error_msg": str(err)}
        }
    return jsonify(response_body)
