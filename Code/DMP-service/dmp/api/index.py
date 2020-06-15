#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD
import time
from datetime import datetime
from flask import (Blueprint,
                   jsonify,
                   current_app,
                   request
                   )
from dmp.utils.task import add
from dmp.models import *
from dmp.extensions import db
from dmp.utils import CM_tools,resp_hanlder
from dmp.utils.task import test_cm

index = Blueprint("index", __name__)


import cm_client as cm

@index.route('/modelhealth/', methods=["GET"], defaults={"desc": "组件健康状态"})
def modelhealth(desc):
    if request.method == "GET":
        try:
            cm = CM_tools()
            res = cm.get_model_health()
            return resp_hanlder(result= res)
        except Exception as err:
            return resp_hanlder(err=err)


@index.route('/disk_io/', methods=["GET"], defaults={"desc": "集群磁盘IO"})
def disk_io(desc):
    if request.method == "GET":
        try:
            time_interval = request.json.get("time_interval")
            res = cm.get_disk_IO(time_interval)
            return resp_hanlder(result=res)
        except Exception as err:
            return resp_hanlder(err=err)



@index.route('/network_io/', methods=["GET"], defaults={"desc": "集群网络IO"})
def network_io(desc):
    if request.method == "GET":
        try:
            time_interval = request.json.get("time_interval")
            res = cm.get_network_IO(time_interval)
            return resp_hanlder(result=res)
        except Exception as err:
            return resp_hanlder(err=err)


@index.route('/cpu_usage/', methods=["GET"], defaults={"desc": "组件健康状态"})
def cpu_usage(desc):
    if request.method == "GET":
        try:
            time_interval = request.json.get("time_interval")
            res = cm.get_model_health(time_interval)
            return resp_hanlder(result=res)
        except Exception as err:
            return resp_hanlder(err=err)


@index.route('/hdfs_io/', methods=["GET"], defaults={"desc": "组件健康状态"})
def hdfs_io(desc):
    if request.method == "GET":
        try:
            time_interval = request.json.get("time_interval")
            res = cm.get_model_health(time_interval)
            return resp_hanlder(result=res)
        except Exception as err:
            return resp_hanlder(err=err)


@index.route('/disk_io_test/', methods=["GET"], defaults={"desc": "组件健康状态"})
def get_disk_IO_test(desc):
    # time_interval = 3600
    # test_cm( time_interval)
    # res = test_cm.dealy(3600)
    import pycurl
    from urllib.parse import urlencode
    try:
        from io import BytesIO
    except ImportError:
        from StringIO import StringIO as BytesIO

    c = pycurl.Curl()


    buffer = BytesIO()
    c.setopt(c.URL, 'http://192.168.3.140:7180/api/v19/timeseries')
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.HTTPAUTH, c.HTTPAUTH_BASIC)
    c.setopt(c.USERNAME, 'admin')
    c.setopt(c.PASSWORD, 'admin')
    time_interval = 3600
    from_time = datetime.fromtimestamp(
        time.time() - int(time_interval))
    to_time = datetime.fromtimestamp(time.time())
    query = "select total_read_bytes_rate_across_disks, total_write_bytes_rate_across_disks where category = CLUSTER"
    post_data  ={
        "from":from_time,
        "to":to_time,
        "query":query
    }
    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()
    print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
    print(buffer.getvalue())
    c.close()

    return resp_hanlder(result=buffer.getvalue().decode())
