#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/25
# @Author  : SHTD 


def job_hanlder(reader,writer):
    job_json = {
        "job":{
            "setting":{
                "speend":{
                    "channel":3
                }
            },
            "content":{
                reader:reader,
                writer:writer
            }
        }
    }
    return job_json