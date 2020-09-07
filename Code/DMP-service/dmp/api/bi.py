#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

from flask import Blueprint,request
from sqlalchemy import literal,union,desc,exists,and_,or_
from validator import create_validator
from dmp.extensions import db
from dmp.models import Dashboard, DashboardArchive,Users,DashboardStar,ArchiveStar
from dmp.utils import resp_hanlder
from dmp.utils.validators.bi import Get_dashboards_and_archives_validator

bi = Blueprint("bi", __name__)


@bi.route("/dashboards", methods=["GET"])
def get_dashboards_and_archives():
    current_user_id = 1
    request_json = request.json
    valid = Get_dashboards_and_archives_validator(request_json)
    if not valid.is_valid():
        return resp_hanlder(code=201, msg=valid.str_errors)
    upper_dmp_dashboard_archive_id = request_json.get("upper_dmp_dashboard_archive_id",None)
    is_owner = request_json.get("is_owner",False)
    state = request_json.get("state","012")
    states = list(str(state))
    name = request_json.get("name",None)
    pagenum = request_json.get("pagenum",1)
    pagesize = request_json.get("pagesize",10)

    dashboards_filters = {
            Dashboard.upper_dmp_dashboard_archive_id == upper_dmp_dashboard_archive_id,
            Dashboard.release.in_(states)
            }

    archives_filters = {
            DashboardArchive.upper_dmp_dashboard_archive_id == upper_dmp_dashboard_archive_id,
            }

    if is_owner == True:
        dashboards_filters.add(Dashboard.created_dmp_user_id==current_user_id)
        archives_filters.add(DashboardArchive.created_dmp_user_id==current_user_id)

    if name != None:
        dashboards_filters.add(Dashboard.dmp_dashboard_name.like("%"+name+"%"))
        archives_filters.add(DashboardArchive.dashboard_archive_name.like("%"+name+"%"))


    dashboards = db.session.query(Dashboard.id.label("id"),
            literal("dashboard").label("type"),
            Dashboard.dmp_dashboard_name.label("name"),
            Dashboard.description.label("description"),
            Dashboard.release.label("release"),
            db.session.query(DashboardStar.id).filter(and_(DashboardStar.dmp_dashboard_id==Dashboard.id,DashboardStar.dmp_user_id==current_user_id)).exists().label("is_star"),
            Dashboard.upper_dmp_dashboard_archive_id.label("upper_dmp_dashboard_archive_id"),
            db.session.query(Users.dmp_username).filter(Users.id == Dashboard.created_dmp_user_id).subquery().c.dmp_username.label("created_dmp_user_name"),
            Dashboard.created_dmp_user_id.label("created_dmp_user_id"),
            Dashboard.created_on.label("created_on"),
           Dashboard.changed_on.label("changed_on")
           ).filter(*dashboards_filters)

    archives = db.session.query(DashboardArchive.id.label("id"),
            literal("archive").label("type"),
            DashboardArchive.dashboard_archive_name.label("name"),
            literal("-").label("description"),
            literal("-").label("release"),
            exists().where(and_(ArchiveStar.dmp_archive_id ==DashboardArchive.id,ArchiveStar.dmp_user_id==current_user_id)).label("is_star"),
            DashboardArchive.upper_dmp_dashboard_archive_id.label("upper_dmp_dashboard_archive_id"),
            db.session.query(Users.dmp_username).filter(Users.id == Dashboard.created_dmp_user_id).subquery().c.dmp_username.label("created_dmp_user_name"),
            DashboardArchive.created_dmp_user_id.label("created_dmp_user_id"),
            DashboardArchive.created_on.label("created_on"),
            DashboardArchive.changed_on.label("changed_on")
            ).filter(*archives_filters)

    dashboards_and_archives = dashboards.union(archives)
    count = dashboards_and_archives.count()
    data = [d._asdict() for d in dashboards_and_archives.order_by(desc("is_star"),desc("changed_on")).offset((pagenum-1)*pagesize).limit(pagesize)]
    res = {
        "data_count":count,
        "pagenum":pagenum,
        "pagesize":pagesize,
        "data":data
        }
    return resp_hanlder(result=res)









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
