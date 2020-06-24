#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD
import time
from datetime import datetime
from flask import Blueprint,current_app,request
from sqlalchemy import func

from dmp.utils.job_task import add
from dmp.models import *
from dmp.extensions import db
from dmp.utils import CM_tools,resp_hanlder


index = Blueprint("index", __name__)


@index.route("/case_count/",methods=["GET"],defaults={"desc": "案例数据量信息"})
def case_count(desc):
    counts = db.session.query(DataTable.dmp_case_id,func.sum(DataTable.db_data_count)).group_by(DataTable.dmp_case_id).all()
    data = [ {"case_name":Case.get(case_id).dmp_case_name,"count":count}  for case_id,count in counts ]
    return resp_hanlder(result=data)

@index.route("/case_table/",methods=["GET"],defaults={"desc": "案例数据表信息"})
def case_table(desc):
    counts = db.session.query(DataTable.dmp_case_id,func.count(DataTable.dmp_case_id)).group_by(DataTable.dmp_case_id).all()
    data = [ {"case_name":Case.get(case_id).dmp_case_name,"count":count}  for case_id,count in counts ]
    return resp_hanlder(result=data)

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
            cm = CM_tools()
            res = cm.get_disk_IO(time_interval)
            return resp_hanlder(result=res)
        except Exception as err:
            return resp_hanlder(err=err)



@index.route('/network_io/', methods=["GET"], defaults={"desc": "集群网络IO"})
def network_io(desc):
    if request.method == "GET":
        try:
            time_interval = request.json.get("time_interval")
            cm = CM_tools()
            res = cm.get_network_IO(time_interval)
            return resp_hanlder(result=res)
        except Exception as err:
            return resp_hanlder(err=err)


@index.route('/cpu_usage/', methods=["GET"], defaults={"desc": "组件健康状态"})
def cpu_usage(desc):
    if request.method == "GET":
        try:
            time_interval = request.json.get("time_interval")
            cm = CM_tools()
            res = cm.get_cpu_usage(time_interval)
            return resp_hanlder(result=res)
        except Exception as err:
            return resp_hanlder(err=err)


@index.route('/hdfs_io/', methods=["GET"], defaults={"desc": "组件健康状态"})
def hdfs_io(desc):
    if request.method == "GET":
        try:
            time_interval = request.json.get("time_interval")
            cm = CM_tools()
            res = cm.get_hdfs_IO(time_interval)
            return resp_hanlder(result=res)
        except Exception as err:
            return resp_hanlder(err=err)


@index.route('/hdfs_disk_usage/', methods=["GET"], defaults={"desc": "HDFS磁盘占用"})
def get_hdfs_disk_usage(desc):
    from dmp.utils import CM_tools
    the_cm = CM_tools()
    res = the_cm.get_hdfs_disk_usage(time_interval=60)
    return resp_hanlder(result=res)