#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

from flask import Blueprint

ds = Blueprint("ds", __name__)

@ds.route("/dataservices",methods=["GET"])
def get_data_services():
    ...


@ds.route("/dataservices/<id:int>",methods=["GET"])
def get_data_service_by_id():
    ...

@ds.route("/dataservices",methods=["POST"])
def add_data_services():
    ...

@ds.route("/dataservices/<id:int>",methods=["PUT"])
def update_data_service_by_id():
    ...

@ds.route("/dataservices/<id:int>",methods=["DELETE"])
def delete_data_service_by_id():
    ...

@ds.route("/api/<api:path>",methods=["GET","POST"])
def get_data_by_data_service():
    ...
