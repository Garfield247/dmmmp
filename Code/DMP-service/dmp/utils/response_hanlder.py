#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD 


response_code = {
    0:"success",
    101:"required_parameter_missing",
    201:"Invalid_token",
    999:"unknow_error"
}


def resp_hanlder(code,msg,result):
    response_body = {
        "status":code,
        "msg":response_code.get(code) if not msg else msg,
        "results":result
    }
