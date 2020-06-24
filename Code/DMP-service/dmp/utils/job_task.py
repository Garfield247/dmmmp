#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD
import json
import os
import uuid

from flask import current_app
from dmp.extensions import celery


@celery.task
def add(x, y):
    return x + y


@celery.task
def job_hanlder(reader, writer,func=None,meta=None):
    job_file_name = "dmp_data_job_" + str(uuid.uuid1())
    job_file_path = os.path.join(current_app.config.get("DATAX_JOB_PATH"), job_file_name)
    job_json = {
        "job": {
            "setting": {
                "speed": {
                    "channel": 3
                }
            },
            "content": [{
                "reader": reader,
                "writer": writer
            }]
        }
    }
    current_app.logger.info(job_json)
    with open(job_file_path, "w", encoding="utf-8") as fp:
        fp.write(json.dumps(job_json, ensure_ascii=False, indent=4))

    task_commit_commamd = "python {Datax_path}/bin3/datax.py {Datax_Job_path}"
    os.system(task_commit_commamd.format(Datax_path=current_app.config.get("DATAX_HOME"), Datax_Job_path=job_file_path))
    if func and meta:
        func(meta)
    elif func:
        func()
    else:
        pass


