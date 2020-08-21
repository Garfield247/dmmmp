#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

from flask import Blueprint

bi = Blueprint("bi", __name__)


@bi.route("/dashboards", methods=["GET"])
def get_dashboards_and_archives():
    ...


@bi.route("/dashboards", methods=["POST"])
def add_dashboard():
    ...


@bi.route("/dashboards/<id:int>", methods=["GET"])
def get_dashboard_by_id():
    ...


@bi.route("/dashboards/<id:int>", methods=["PUT"])
def update_dashboard_by_id():
    ...


@bi.route("/dashboards/<id:int>", methods=["DELETE"])
def delete_dashboard_by_id():
    ...


@bi.route("/archives", methods=["POST"])
def add_archive():
    ...


@bi.route("/archives/<id:int>", methods=["PUT"])
def update_archive_by_id():
    ...


@bi.route("/archives/<id:int>", methods=["DELETE"])
def delete_archive_by_id():
    ...


@bi.route("/charts", methods=["POST"])
def add_chart():
    ...


@bi.route("/charts/<id:int>", methods=["PUT"])
def update_charts_by_id():
    ...
