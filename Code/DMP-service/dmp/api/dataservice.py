#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

from flask import Blueprint

ds = Blueprint("ds", __name__)


@ds.route("/dataservices", methods=["GET"])
def get_data_services():
    pass


@ds.route("/dataservices/<int:id>", methods=["GET"])
def get_data_service_by_id():
    pass


@ds.route("/dataservices", methods=["POST"])
def add_data_services():
    pass


@ds.route("/dataservices/<int:id>", methods=["PUT"])
def update_data_service_by_id():
    pass


@ds.route("/dataservices/<int:id>", methods=["DELETE"])
def delete_data_service_by_id():
    pass


@ds.route("/api/<path:api>", methods=["GET", "POST"])
def get_data_by_data_service():
    pass
