#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD 

from flask import jsonify

response_code = {
    0:"success",
    # 参数类错误
    101:"required_parameter_missing",
    # 权限类错误
    201:"Invalid_Token",
    301:"Permission_Denied",
    # 对象类错误
    404: "Item_Does_Not_Exist",
    # 数据库类错误
    501:"Connection_Failed",
    502:"Database_Occupied",
    # 其他错误
    999:"Other_Error"
}


def resp_hanlder(**option):
    msg = option.get("msg")
    result = option.get("result")
    err = option.get("err")
    code = 999 if err and not option.get("code") else option.get("code",0)
    response_body = {
        "status":code,
        "msg":response_code.get(code) if not msg else msg,
        "results":result if not err else {"error_msg":str(err)}
    }
    return  jsonify(response_body)
