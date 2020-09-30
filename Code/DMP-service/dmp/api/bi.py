#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

from flask import Blueprint, request

from sqlalchemy import literal,and_,or_,exists,union,desc,union_all
from sqlalchemy import desc as desc_
from dmp.extensions import db
from dmp.models import Dashboard, DashboardArchive, Users, DashboardStar, ArchiveStar,Chart,UserDashboard
from dmp.utils import resp_hanlder
from dmp.utils.put_data import PuttingData
from dmp.utils.validators.bi import Get_dashboards_and_archives_validator

bi = Blueprint("bi", __name__)


@bi.route("/dashboards", methods=["GET"],defaults={"desc": {"interface_name": "查询多个文件夹和看板服务", "is_permission": True, "permission_belong": 0}})
def get_dashboards_and_archives(desc):
    """
    查询多个文件夹和看板服务

    ---
    tags:
      - BI
    parameters:
      - name: upper_dmp_dashboard_archive_id
        type: int
        required: false
        description: 父文件夹
      - name: is_owner
        type: bool
        required: true
        description: 是否是我的
      - name: state
        type: int
        required: false
        description: 发布状态
      - name: name
        type: string
        required: false
        description: 要检索的看板名或用户名
      - name: pagenum
        type: int
        required: true
        description: 页码
      - name: pagesize
        type: int
        required: true
        description: 每页内容数量
    responses:
      0:
        description: OK!
	"""
    auth_token = request.headers.get('Authorization')
    current_user_id = Users.decode_auth_token(auth_token)
    # current_user_id = 1
    request_json = request.json if request.json else {}
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
            exists().where(and_(UserDashboard.dmp_dashboard_id ==Dashboard.id,UserDashboard.dmp_user_id==current_user_id)).label("is_index"),
            Dashboard.upper_dmp_dashboard_archive_id.label("upper_dmp_dashboard_archive_id"),
            db.session.query(Users.dmp_username).filter(Users.id == Dashboard.created_dmp_user_id).subquery().c.dmp_username.label("created_dmp_user_name"),
            Dashboard.created_dmp_user_id.label("created_dmp_user_id"),
            db.session.query(Users.dmp_username).filter(Users.id == Dashboard.changed_dmp_user_id).subquery().c.dmp_username.label("changed_dmp_user_name"),
            Dashboard.changed_dmp_user_id.label("changed_dmp_user_id"),
            Dashboard.created_on.label("created_on"),
           Dashboard.changed_on.label("changed_on")
           ).filter(*dashboards_filters)

    archives = db.session.query(DashboardArchive.id.label("id"),
            literal("archive").label("type"),
            DashboardArchive.dashboard_archive_name.label("name"),
            literal("-").label("description"),
            literal("-").label("release"),
            exists().where(and_(ArchiveStar.dmp_archive_id ==DashboardArchive.id,ArchiveStar.dmp_user_id==current_user_id)).label("is_star"),
            literal("-").label("is_index"),
            DashboardArchive.upper_dmp_dashboard_archive_id.label("upper_dmp_dashboard_archive_id"),
            db.session.query(Users.dmp_username).filter(Users.id == Dashboard.created_dmp_user_id).subquery().c.dmp_username.label("created_dmp_user_name"),
            DashboardArchive.created_dmp_user_id.label("created_dmp_user_id"),
            db.session.query(Users.dmp_username).filter(Users.id == Dashboard.changed_dmp_user_id).subquery().c.dmp_username.label("changed_dmp_user_name"),
            DashboardArchive.changed_dmp_user_id.label("changed_dmp_user_id"),
            DashboardArchive.created_on.label("created_on"),
            DashboardArchive.changed_on.label("changed_on")
            ).filter(*archives_filters)

    dashboards_and_archives = dashboards.union(archives)
    count = dashboards_and_archives.count()
    data = [d._asdict() for d in dashboards_and_archives.order_by(desc_("is_index"),desc_("is_star"),desc_("changed_on")).offset((pagenum-1)*pagesize).limit(pagesize)]
    res = {
        "data_count":count,
        "pagenum":pagenum,
        "pagesize":pagesize,
        "data":data
        }
    return resp_hanlder(result=res)

@bi.route("/index", methods=["GET"],defaults={"desc": {"interface_name": "获取首页看板", "is_permission": True, "permission_belong": 0}})
def get_index_dashboards(desc):
    """
    获取首页看板

    ---
    tags:
      - BI
    parameters:
      - name: 无
        type: int
        required: false
        description: 无需参数
    responses:
      0:
        description: OK!
    """
    auth_token = request.headers.get('Authorization')
    current_user_id = Users.decode_auth_token(auth_token)
    index_dashboards = None
    ud = UserDashboard.query.filter_by(dmp_user_id==current_user_id).first()
    index_dashboards_id = ud.dmp_dashboard_id if ud else None
    if index_dashboards_id:
        index_dashboards_obj = db.session.query(Dashboard.id.label("id"),
            literal("dashboard").label("type"),
            Dashboard.dmp_dashboard_name.label("name"),
            Dashboard.charts_position.label("charts_position"),
            Dashboard.description.label("description"),
            Dashboard.release.label("release"),
            db.session.query(DashboardStar.id).filter(and_(DashboardStar.dmp_dashboard_id==Dashboard.id,DashboardStar.dmp_user_id==current_user_id)).exists().label("is_star"),
            exists().where(and_(UserDashboard.dmp_dashboard_id ==Dashboard.id,UserDashboard.dmp_user_id==current_user_id)).label("is_index"),
            Dashboard.upper_dmp_dashboard_archive_id.label("upper_dmp_dashboard_archive_id"),
            db.session.query(Users.dmp_username).filter(Users.id == Dashboard.created_dmp_user_id).subquery().c.dmp_username.label("created_dmp_user_name"),
            Dashboard.created_dmp_user_id.label("created_dmp_user_id"),
            Dashboard.created_on.label("created_on"),
           Dashboard.changed_on.label("changed_on")
           ).filter(Dashboard.id==index_dashboards_id).first()
        index_dashboards = index_dashboards_obj._asdict() if index_dashboards_obj else None
    return resp_hanlder(code=0,result={"index":index_dashboards})

@bi.route("/dashboards/",methods=["POST"], defaults={"desc": {"interface_name": "创建看板", "is_permission": True, "permission_belong": 0}})
def add_dashboard(desc):
    '''创建看板'''
    try:
        auth_token = request.headers.get('Authorization')
        res = PuttingData.get_obj_data(Users, auth_token)
        if not isinstance(res, dict):
            return resp_hanlder(code=999)
        data = request.json
        if data == None:
            return resp_hanlder(code=999)
        dmp_dashboard_name = data.get('dmp_dashboard_name')
        charts_position = data.get('charts_position')
        upper_dmp_dashboard_archive_id = data.get('upper_dmp_dashboard_archive_id')
        if dmp_dashboard_name:
            dashboard_obj = Dashboard(
                dmp_dashboard_name=dmp_dashboard_name,
                upper_dmp_dashboard_archive_id=upper_dmp_dashboard_archive_id,
                charts_position=charts_position,
                release=0,
                created_dmp_user_id=res.get('id'),
                changed_dmp_user_id=res.get('id')
            )
            db.session.add(dashboard_obj)
            db.session.commit()
            return resp_hanlder(code=0, msg='数据看板创建成功.',
                                result=dashboard_obj.dashboard_to_dict())
        else:
            return resp_hanlder(code=999, msg='请确认新创建的看板名称是否存在并确认其是否正确.')
    except Exception as err:
        db.session.rollback()
        return resp_hanlder(code=999, err=str(err))

@bi.route("/dashboards/<int:dashboard_id>",methods=["GET"], defaults={"desc": {"interface_name": "获取单一看板信息", "is_permission": True, "permission_belong": 0}})
def get_dashboard_by_id(dashboard_id):
    """
    获取但一看板信息

    ---
    tags:
      - BI
    parameters:
      - name: dashboard_id
        type: int
        required: true
        description: 要获取的看板ID
    responses:
      0:
        description: OK
	"""
    if Dashboard.exist_item_by_id(dashboard_id):
        dashboards_obj = db.session.query(Dashboard.id.label("id"),
            literal("dashboard").label("type"),
            Dashboard.dmp_dashboard_name.label("name"),
            Dashboard.description.label("description"),
            Dashboard.charts_position.label("charts_position"),
            Dashboard.release.label("release"),
            db.session.query(DashboardStar.id).filter(and_(DashboardStar.dmp_dashboard_id==Dashboard.id,DashboardStar.dmp_user_id==current_user_id)).exists().label("is_star"),
            exists().where(and_(UserDashboard.dmp_dashboard_id ==Dashboard.id,UserDashboard.dmp_user_id==current_user_id)).label("is_index"),
            Dashboard.upper_dmp_dashboard_archive_id.label("upper_dmp_dashboard_archive_id"),
            db.session.query(Users.dmp_username).filter(Users.id == Dashboard.created_dmp_user_id).subquery().c.dmp_username.label("created_dmp_user_name"),
            Dashboard.created_dmp_user_id.label("created_dmp_user_id"),
            Dashboard.created_on.label("created_on"),
           Dashboard.changed_on.label("changed_on")
           ).filter(Dashboard.id==index_dashboards_id).first()
        dashboards = dashboards_obj._asdict() if dashboards_obj else None
        return resp_hanlder(code=0, result={"data":dashboards})
    else:
        return resp_hanlder(code=999,msg="看板不存在或已被删除")


@bi.route("/dashboards/<int:id>",methods=["PUT"], defaults={"desc": {"interface_name": "修改看板", "is_permission": True, "permission_belong": 0}})
def update_dashboard_by_id(id, desc):
    '''修改看板'''
    try:
        auth_token = request.headers.get('Authorization')
        res = PuttingData.get_obj_data(Users, auth_token)
        if not isinstance(res, dict):
            return resp_hanlder(code=999)
        data = request.json
        if data == None:
            return resp_hanlder(code=999)
        dmp_dashboard_name = data.get('dmp_dashboard_name')
        description = data.get('description')
        charts_position = data.get('charts_position')
        release = data.get('release')
        upper_dmp_dashboard_archive_id = data.get('upper_dmp_dashboard_archive_id')
        dashboard_obj = Dashboard.query.filter(Dashboard.id == id).first()

        if dashboard_obj.created_dmp_user_id == res.get('id'):
            if dmp_dashboard_name and id:
                dashboard_obj.dmp_dashboard_name = dmp_dashboard_name
                dashboard_obj.description = description
                dashboard_obj.charts_position = charts_position
                dashboard_obj.release = release
                dashboard_obj.upper_dmp_dashboard_archive_id = upper_dmp_dashboard_archive_id
                dashboard_obj.changed_dmp_user_id = res.get('id')
                db.session.commit()
                return resp_hanlder(code=0, msg='看板数据修改成功.',
                                    result=dashboard_obj.dashboard_to_dict())
            else:
                return resp_hanlder(code=999, msg='请确认看板名称是否存在并确认其是否正确.')
        else:
            return resp_hanlder(code=301, msg='没有权限修改其他看板信息.')
    except Exception as err:
        db.session.rollback()
        return resp_hanlder(code=999, err=str(err))

@bi.route("/dashboards/<int:id>",methods=["DELETE"], defaults={"desc": {"interface_name": "删除看板", "is_permission": True, "permission_belong": 0}})
def delete_dashboard_by_id(id, desc):
    '''删除看板'''
    try:
        auth_token = request.headers.get('Authorization')
        res = PuttingData.get_obj_data(Users, auth_token)
        if not isinstance(res, dict):
            return resp_hanlder(code=999)
        del_dashboard_obj = Dashboard.query.filter(Dashboard.id == id).first()

        if del_dashboard_obj.created_dmp_user_id == res.get('id') or res.get('id') == 1:
            if del_dashboard_obj and id:
                # 封装的delete方法
                del_dashboard_obj.delete()
                return resp_hanlder(code=0, msg='看板删除成功.')
            else:
                return resp_hanlder(code=999, msg='看板ID错误或对象不存在,请重新确认.')
        else:
            return resp_hanlder(code=999, msg='没有权限删除看板,请联系超级管理员.')
    except Exception as err:
        db.session.rollback()
        return resp_hanlder(code=999, err=str(err))

@bi.route("/archives/",methods=["POST"], defaults={"desc": {"interface_name": "创建文件夹", "is_permission": True, "permission_belong": 0}})
def add_archive(desc):
    '''创建文件夹'''
    if request.method == 'POST':
        try:
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            if not isinstance(res, dict):
                return resp_hanlder(code=999)
            data = request.json
            if data == None:
                return resp_hanlder(code=999)
            dashboard_archive_name = data.get('dashboard_archive_name')

            upper_dmp_dashboard_archive_id = data.get('upper_dmp_dashboard_archive_id')
            if upper_dmp_dashboard_archive_id:
                upper_archive_obj = DashboardArchive.query.filter(
                                        DashboardArchive.id == upper_dmp_dashboard_archive_id).first()
                if upper_archive_obj:
                    if upper_archive_obj.created_dmp_user_id == res.get('id'):
                        da_obj = DashboardArchive(
                            dashboard_archive_name=dashboard_archive_name,
                            upper_dmp_dashboard_archive_id=upper_dmp_dashboard_archive_id,
                            created_dmp_user_id=res.get('id'),
                            changed_dmp_user_id=res.get('id')
                        )
                        db.session.add(da_obj)
                        db.session.commit()
                        return resp_hanlder(code=0, msg='子看板文件夹创建成功.',
                                            result=da_obj.dashboard_archive_to_dict())
                    else:
                        return resp_hanlder(code=999, msg='无法创建该文件夹对象.')
                else:
                    return resp_hanlder(code=999, msg='父文件夹对象不存在,请重新操作.')
            else:
                if dashboard_archive_name:
                    da_obj = DashboardArchive(
                        dashboard_archive_name=dashboard_archive_name,
                        upper_dmp_dashboard_archive_id=upper_dmp_dashboard_archive_id,
                        created_dmp_user_id=res.get('id'),
                        changed_dmp_user_id=res.get('id')
                    )
                    db.session.add(da_obj)
                    db.session.commit()
                    return resp_hanlder(code=0, msg='看板文件夹创建成功.',
                                        result=da_obj.dashboard_archive_to_dict())
                else:
                    return resp_hanlder(code=999, msg='请确认新创建的看板文件夹名称是否存在并确认其是否正确.')

        except Exception as err:
            db.session.rollback()
            return resp_hanlder(err=err)

@bi.route("/archives/<int:id>",methods=["PUT"], defaults={"desc": {"interface_name": "修改文件夹信息", "is_permission": True, "permission_belong": 0}})
def update_archive_by_id(id, desc):
    '''修改文件夹信息'''
    if request.method == 'PUT':
        try:
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            if not isinstance(res, dict):
                return resp_hanlder(code=999)
            data = request.json
            if data == None:
                return resp_hanlder(code=999)
            dashboard_archive_name = data.get('dashboard_archive_name')
            update_dashboard_archive_obj = DashboardArchive.query.filter(DashboardArchive.id == id).first()

            if DashboardArchive.created_dmp_user_id == res.get('id'):
                if dashboard_archive_name and update_dashboard_archive_obj:
                    update_dashboard_archive_obj.dashboard_archive_name = dashboard_archive_name
                    update_dashboard_archive_obj.changed_dmp_user_id = res.get('id')
                    db.session.commit()
                    return resp_hanlder(code=0, msg='看板文件夹信息修改成功.',
                                        result=update_dashboard_archive_obj.dashboard_archive_to_dict())
                else:
                    return resp_hanlder(code=999, msg='请正确输入修改文件夹信息.')
            else:
                return resp_hanlder(code=301, msg='没有权限修改其他看板文件夹信息.')
        except Exception as err:
            db.session.rollback()
            return resp_hanlder(code=999, err=str(err))

@bi.route("/archives/<int:id>",methods=["DELETE"], defaults={"desc": {"interface_name": "删除文件夹", "is_permission": True, "permission_belong": 0}})
def delete_archive_by_id(id, desc):
    '''删除文件夹'''
    try:
        auth_token = request.headers.get('Authorization')
        res = PuttingData.get_obj_data(Users, auth_token)
        if not isinstance(res, dict):
            return resp_hanlder(code=999)
        del_archive_obj = DashboardArchive.query.filter(DashboardArchive.id == id).first()

        if del_archive_obj.created_dmp_user_id == res.get('id') or res.get('id') == 1:
            if del_archive_obj and id:
                del_archive_obj.delete()
                return resp_hanlder(code=0, msg='看板文件夹删除成功.')
            else:
                return resp_hanlder(code=999, msg='看板文件夹ID错误或对象不存在,请重新确认.')
        else:
            return resp_hanlder(code=999, msg='没有权限删除看板文件夹,请联系超级管理员.')
    except Exception as err:
        db.session.rollback()
        return resp_hanlder(code=999, err=str(err))

@bi.route("/charts/",methods=["POST"], defaults={"desc": {"interface_name": "添加图表接口", "is_permission": True, "permission_belong": 0}})
def add_chart(desc):
    '''添加图表接口'''
    try:
        auth_token = request.headers.get('Authorization')
        res = PuttingData.get_obj_data(Users, auth_token)
        if not isinstance(res, dict):
            return resp_hanlder(code=999)
        data = request.json
        if data == None:
            return resp_hanlder(code=999)
        chart_name = data.get('chart_name')
        dmp_data_table_id = data.get('dmp_data_table_id')
        query_string = data.get('query_string')
        chart_data = data.get('chart_data')
        chart_type = data.get('chart_type')
        chart_params = data.get('chart_params')
        description = data.get('description')
        dmp_dashboard_id = data.get('dmp_dashboard_id')

        if chart_name and chart_type and dmp_dashboard_id and dmp_data_table_id:
            chart_obj = Chart(
                chart_name=chart_name,
                dmp_data_table_id=dmp_data_table_id,
                query_string=query_string,
                chart_data=chart_data,
                chart_type=chart_type,
                params=chart_params,
                description=description,
                dmp_dashboard_id=dmp_dashboard_id,
                created_dmp_user_id=res.get('id'),
                changed_dmp_user_id=res.get('id')
            )
            db.session.add(chart_obj)
            db.session.commit()
            return resp_hanlder(code=0, msg='图表添加成功.', result=chart_obj.chart_to_dict())
        else:
            return resp_hanlder(code=999, msg='缺少必要参数,并确定其参数是否正确.')
    except Exception as err:
        db.session.rollback()
        return resp_hanlder(code=999, err=str(err))

@bi.route("/charts/<int:id>",methods=["PUT"], defaults={"desc": {"interface_name": "修改图表", "is_permission": True, "permission_belong": 0}})
def update_charts_by_id(id, desc):
    '''修改图表'''
    if request.method == 'PUT':
        try:
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            if not isinstance(res, dict):
                return resp_hanlder(code=999)
            data = request.json
            if data == None:
                return resp_hanlder(code=999)
            chart_name = data.get('chart_name')
            dmp_data_table_id = data.get('dmp_data_table_id')
            query_string = data.get('query_string')
            chart_data = data.get('chart_data')
            chart_type = data.get('chart_type')
            chart_params = data.get('chart_params')
            description = data.get('description')
            dmp_dashboard_id = data.get('dmp_dashboard_id')
            chart_obj = Chart.query.filter(Chart.id == id).first()

            if Chart.created_dmp_user_id == res.get('id'):
                if chart_name and chart_type and dmp_dashboard_id and chart_obj:
                    chart_obj.chart_name = chart_name
                    chart_obj.dmp_data_table_id = dmp_data_table_id
                    chart_obj.query_string = query_string
                    chart_obj.chart_data = chart_data
                    chart_obj.chart_type = chart_type
                    chart_obj.chart_params = chart_params
                    chart_obj.description = description
                    chart_obj.dmp_dashboard_id = dmp_dashboard_id
                    chart_obj.changed_dmp_user_id = res.get('id')
                    db.session.commit()
                else:
                    return resp_hanlder(code=999, msg='请正确输入修改图表信息.')
            else:
                return resp_hanlder(code=301, msg='没有权限修改其他图表信息.')
        except Exception as err:
            db.session.rollback()
            return resp_hanlder(code=999, err=str(err))

@bi.route("/charts/<int:id>",methods=["DELETE"], defaults={"desc": {"interface_name": "删除图表", "is_permission": True, "permission_belong": 0}})
def delete_charts_by_id(id, desc):
    '''删除图表'''
    try:
        auth_token = request.headers.get('Authorization')
        res = PuttingData.get_obj_data(Users, auth_token)
        if not isinstance(res, dict):
            return resp_hanlder(code=999)
        del_chart_obj = Chart.query.filter(Chart.id == id).first()

        if del_chart_obj.created_dmp_user_id == res.get('id') or res.get('id') == 1:
            if del_chart_obj and id:
                db.session.delete(del_chart_obj)
                db.session.commit()
                return resp_hanlder(code=0, msg='图表删除成功.')
            else:
                return resp_hanlder(code=999, msg='图表ID错误或对象不存在,请重新确认.')
        else:
            return resp_hanlder(code=999, msg='没有权限删除图表,请联系超级管理员.')
    except Exception as err:
        db.session.rollback()
        return resp_hanlder(code=999, err=str(err))


@bi.route("/index/<int:dashboard_id>", methods=["POST"],defaults={"desc": {"interface_name": "设置首页", "is_permission": True, "permission_belong": 0}})
def set_index(desc,dashboard_id):
    """
    设置首页

    ---
    tags:
      - BI
    parameters:
      - name: dashboard_id
        type: int
        required: true
        description: 要设置为首页的看板ID
    responses:
      0:
        description: ok
    """
    auth_token = request.headers.get('Authorization')
    current_user_id = Users.decode_auth_token(auth_token)

    if Dashboard.exist_item_by_id(dashboard_id):

        UserDashboard.query.filter_by(dmp_user_id = current_user_id).delete()

        index_page = UserDashboard(
            dmp_user_id = current_user_id,
            dmp_dashboard_id = dashboard_id
                )
        index_page.save()
        return resp_hanlder(code=0,result="OK")


@bi.route("/index/", methods=["DELETE"],defaults={"desc": {"interface_name": "取消设置首页", "is_permission": True, "permission_belong": 0}})
def del_index(desc):
    """
    取消设置首页

    ---
    tags:
      - BI
    parameters:
      - name: 无
        in: <++>
        type: string
        required: false
        description: 不需要参数
    responses:
      0:
        description: ok
    """
    auth_token = request.headers.get('Authorization')
    current_user_id = Users.decode_auth_token(auth_token)
    if current_user_id:
        UserDashboard.query.filter_by(dmp_user_id = current_user_id).delete()
        return resp_hanlder(code=0,result="OK")


@bi.route("/dashboards_star/<int:dashboard_id>", methods=["POST"],defaults={"desc": {"interface_name": "看板置顶", "is_permission": True, "permission_belong": 0}})
def add_dashboard_star(desc,dashboard_id):
    """
    看板置顶

    ---
    tags:
      - BI
    parameters:
      - name: dashboard_id
        type: int
        required: true
        description: 要置顶的看板的ID
    responses:
      0:
        description: ok
	"""
    auth_token = request.headers.get('Authorization')
    current_user_id = Users.decode_auth_token(auth_token)

    if Dashboard.exist_item_by_id(dashboard_id):
        is_exists = db.session.query(exists().where(and_(DashboardStar.dmp_user_id==current_user_id,DashboardStar.dmp_dashboard_id==dashboard_id))).scalar()
        if not is_exists:
            star = DashboardStar(
                dmp_user_id = current_user_id,
                dmp_dashboard_id = dashboard_id
                    )
            star.save()
            return resp_hanlder(code=0,msg="OK")
        else:
            return resp_hanlder(code=999,msg="看板已置顶")
    else:
        return resp_hanlder(code=999,msg="看板不存在或已被删除")


@bi.route("/dashboards_star/<int:dashboard_id>", methods=["DELETE"],defaults={"desc": {"interface_name": "看板取消置顶", "is_permission": True, "permission_belong": 0}})
def del_dashboard_star(desc,dashboard_id):
    """
    看板取消置顶

    ---
    tags:
      - BI
    parameters:
      - name: dashboard_id
        type: int
        required: true
        description: 要取消置顶的看板ID
    responses:
      0:
        description: ok
	"""
    auth_token = request.headers.get('Authorization')
    current_user_id = Users.decode_auth_token(auth_token)
    if Dashboard.exist_item_by_id(dashboard_id):
        is_exists = db.session.query(exists().where(and_(DashboardStar.dmp_user_id==current_user_id,DashboardStar.dmp_dashboard_id==dashboard_id))).scalar()
        if is_exists:
            DashboardStar.query.filter_by(dmp_user_id=current_user_id,dmp_dashboard_id=dashboard_id).delete()
            return resp_hanlder(code=0,msg="OK")
        else:
            return resp_hanlder(code=999,msg="看板已删除置顶")
    else:
        return resp_hanlder(code=999,msg="看板不存在或已被删除")



@bi.route("/archive_star/<int:archive_id>", methods=["POST"],defaults={"desc": {"interface_name": "文件夹置顶", "is_permission": True, "permission_belong": 0}})
def add_archive_star(desc):
    """
    文件夹置顶

    ---
    tags:
      - BI
    parameters:
      - name: archive_id
        type: int
        required: true
        description: 要置顶的文件夹ID
    responses:
      0:
        description: ok
    """
    auth_token = request.headers.get('Authorization')
    current_user_id = Users.decode_auth_token(auth_token)
    if DashboardArchive.exist_item_by_id(archive_id):
        is_exists = db.session.query(exists().where(and_(ArchiveStar.dmp_user_id==current_user_id,ArchiveStar.dmp_dashboard_id==dashboard_id))).scalar()
        if not is_exists:
            star = ArchiveStar(
                dmp_user_id = current_user_id,
                dmp_archive_id = archive_id
                    )
            star.save()
            return resp_hanlder(code=0,msg="OK")
        else:
            return resp_hanlder(code=999,msg="文件夹已置顶")
    else:
        return resp_hanlder(code=999,msg="文件夹不存在或已被删除")



@bi.route("/archive_star/<int:archive_id>", methods=["DELETE"],defaults={"desc": {"interface_name": "文件夹取消置顶", "is_permission": True, "permission_belong": 0}})
def del_archive_star(desc):
    """
    文件夹取消置顶

    ---
    tags:
      - BI
    parameters:
      - name: archive_id
        type: int
        required: true
        description: 要取消置顶的文件夹ID
    responses:
      0:
        description: ok
	"""
    auth_token = request.headers.get('Authorization')
    current_user_id = Users.decode_auth_token(auth_token)
    if DashboardArchive.exist_item_by_id(archive_id):
        is_exists = db.session.query(exists().where(and_(ArchiveStar.dmp_user_id==current_user_id,ArchiveStar.dmp_dashboard_id==dashboard_id))).scalar()
        if is_exists:
            ArchiveStar.query.filter_by(dmp_user_id=current_user_id,dmp_archive_id=archive_id).delete()
            return resp_hanlder(code=0,msg="OK")
        else:
            return resp_hanlder(code=999,msg="文件夹已置顶")
    else:
        return resp_hanlder(code=999,msg="看板不存在或已被删除")



