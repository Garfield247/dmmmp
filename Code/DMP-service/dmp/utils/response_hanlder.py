#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD 

from flask import jsonify

response_code = {
    0:"success",
    101:"required_parameter_missing",
    201:"Invalid_Token",
    301:"Permission_Denied",
    401:"Connection_Failed",
    402:"Database_Occupied",
    404:"Item_Does_Not_Exist",
    999:"unknow_error"
}


def resp_hanlder(**option):
    code = option.get("code") or 0
    msg = option.get("msg")
    result = option.get("result")
    err = option.get("err")
    response_body = {
        "status":code,
        "msg":response_code.get(code) if not msg else msg,
        "results":result if not err else {"error_msg":str(err)}
    }
    return  jsonify(response_body)
