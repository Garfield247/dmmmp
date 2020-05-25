#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/25
# @Author  : SHTD
import json
from .job_mongodb import mongodb_reader, mongodb_writer
from .job_mysql import mysql_reader, mysql_writer
from .job_hive import hive_reader, hive_writer


def job_hanlder(reader, writer):
    job_json = {
        "job": {
            "setting": {
                "speend": {
                    "channel": 3
                }
            },
            "content": {
                reader: reader,
                writer: writer
            }
        }
    }
    filename = "/root/job/test_job.json"
    with open(filename,"w",encoding="utf-8") as fp:
        fp.write(json.dumps(job_json,ensure_ascii=False))
    return filename
