#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD
import json
import os
import uuid
import time
from datetime import datetime

from flask import current_app
from dmp.extensions import mail
from dmp.extensions import celery

import cm_client as cm

@celery.task
def add(x, y):
    return x + y

@celery.task
def job_hanlder(reader, writer):
    job_file_name = "dmp_data_job_" + str(uuid.uuid1())
    job_file_path = os.path.join(current_app.config.get("DATAX_JOB_PATH"),job_file_name)
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

    with open(job_file_path,"w",encoding="utf-8") as fp:
        fp.write(json.dumps(job_json,ensure_ascii=False,indent=4))

    task_commit_commamd = "python {Datax_path}/bin3/datax.py {Datax_Job_path}"
    os.system(task_commit_commamd.format(Datax_path = current_app.config.get("DATAX_HOME"),Datax_Job_path=job_file_path))

@celery.task
def test_cm(time_interval):

    user = "admin"
    password = "admin"
    host = "192.168.3.140"
    port = 7180
    version = "v19"
    api_url = "http://%s:%d/api/%s" % (host, port, version)
    api_client = cm.ApiClient(api_url)
    services_api_instance = cm.TimeSeriesResourceApi(api_client)
    from_time = datetime.fromtimestamp(
        time.time() - int(time_interval))
    to_time = datetime.fromtimestamp(time.time())
    query = "select total_read_bytes_rate_across_disks, total_write_bytes_rate_across_disks where category = CLUSTER"
    res = services_api_instance.query_time_series(
        _from=from_time, query=query, to=to_time)
    return res
