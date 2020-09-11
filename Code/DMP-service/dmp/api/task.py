#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import Blueprint,request
from dmp.extensions import apscheduler
from dmp.utils.aps_task import update_chart_data
from dmp.utils import uuid_str

task = Blueprint("task",__name__)



@task.route("/chart_data/<task_id>",methods=["GET"])
def get_query_data_tasks(task_id):
    _task = apscheduler.get_job(id=task_id)
    info = {
        "ss"
            }


