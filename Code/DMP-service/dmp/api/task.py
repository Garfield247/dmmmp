#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import Blueprint,request
from dmp.extensions import apscheduler
from dmp.utils.aps_task import task2json, update_chart_data
from dmp.utils.validators.task import Add_query_data_task_validator,Update_query_data_task_validator
from dmp.utils import resp_hanlder,uuid_str

task = Blueprint("task",__name__)



@task.route("/chart_data/<task_id>",methods=["GET"])
def get_query_data_task(task_id):
    _task = apscheduler.get_job(id=task_id)
    return task2json(_task)

@task.route("/chart_data",methods=["POST"])
def add_query_data_task():
    _task_param = request.json
    valid = Add_query_data_task_validator(_task_param)
    if not valid.is_valid():
        return resp_hanlder(code=201,msg=valid.str_errors)
    chart_id = _task_param.get("chart_id")
    time_unit = _task_param.get("time_unit")
    time_value = _task_param.get("time_value")
    task_params = {}
    task_params["id"] = uuid_str()
    task_params["kwargs"] = {"chart_id":chart_id}
    task_params["func"] = update_chart_data
    task_params["trigger"] = "interval"
    task_params[time_unit] = time_value
    print(task_params)
    apscheduler.add_job(**task_params)
    return resp_hanlder(result={"task_id":task_params.get("id")})

@task.route("/chart_data/<task_id>",methods=["PUT"])
def update_query_data_task(task_id):
    current_task = apscheduler.get_job(task_id)
    if current_task:
        _task_param = request.json
        valid = Update_query_data_task_validator(_task_param)
        if not valid.is_valid():
            return resp_hanlder(code=201,msg=valid.str_errors)
        time_unit = _task_param.get("time_unit")
        time_value = _task_param.get("time_value")
        task_params = {}
        task_params[time_unit] = time_value
        current_task.modify(**task_params)
        return resp_hanlder(result="OK")
    else:
        return resp_hanlder(code=999,msg="任务不存在或已被删除")

@task.route("/chart_data/<task_id>",methods=["DELETE"])
def delete_query_data_task(task_id):
    current_task = apscheduler.get_job(task_id)
    if current_task:
        current_task.remove()
        return resp_hanlder(result="OK")
    else:
        return resp_hanlder(code=999,msg="任务不存在或已删除")
