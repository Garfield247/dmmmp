#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

from flask import Blueprint

bi = Blueprint("bi", __name__)


@bi.route("/dashboards", methods=["GET"])
def get_dashboards_and_archives():
    pass


@bi.route("/dashboards", methods=["POST"])
def add_dashboard():
    pass


@bi.route("/dashboards/<int:id>", methods=["GET"])
def get_dashboard_by_id():
    pass


@bi.route("/dashboards/<int:id>", methods=["PUT"])
def update_dashboard_by_id():
    pass


@bi.route("/dashboards/<int:id>", methods=["DELETE"])
def delete_dashboard_by_id():
    pass


@bi.route("/archives", methods=["POST"])
def add_archive():
    pass


@bi.route("/archives/<int:id>", methods=["PUT"])
def update_archive_by_id():
    pass


@bi.route("/archives/<int:id>", methods=["DELETE"])
def delete_archive_by_id():
    pass


@bi.route("/charts", methods=["POST"])
def add_chart():
    pass


@bi.route("/charts/<int:id>", methods=["PUT"])
def update_charts_by_id():
    pass
