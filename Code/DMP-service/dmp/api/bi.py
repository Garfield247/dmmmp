#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

from flask import Blueprint, request

from dmp.extensions import db
from dmp.models import Users
from dmp.models.dmp_chart import Chart
from dmp.models.dmp_dashboard import Dashboard
from dmp.models.dmp_archive import DashboardArchive
from dmp.utils import resp_hanlder
from dmp.utils.put_data import PuttingData

bi = Blueprint("bi", __name__)

@bi.route("/dashboards/",methods=["GET"])
def get_dashboards_and_archives():
    pass

@bi.route("/dashboards/",methods=["POST"])
def add_dashboard():
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

@bi.route("/dashboards/<int:id>",methods=["GET"])
def get_dashboard_by_id(id):
    pass

@bi.route("/dashboards/<int:id>",methods=["PUT"])
def update_dashboard_by_id(id):
    # 修改看板
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

        # 看板只有自己才能修改，别人无权修改
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

@bi.route("/dashboards/<int:id>",methods=["DELETE"])
def delete_dashboard_by_id(id):
    # 删除看板--只有自己和id=1的超级管理员可以删除，其他人没有删除权限
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

@bi.route("/archives/",methods=["POST"])
def add_archive():
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
            # 文件夹ID(父)
            upper_dmp_dashboard_archive_id = data.get('upper_dmp_dashboard_archive_id')

            if upper_dmp_dashboard_archive_id:
                # 如果存在父ID--保证create_id == 自己(当前登录)的id
                # 找到父文件对应的create_id
                # 父文件夹对象
                upper_archive_obj = DashboardArchive.query.filter(
                                        DashboardArchive.id == upper_dmp_dashboard_archive_id).first()
                if upper_archive_obj:
                    # 该父文件夹ID的创建人id等于当前登录用户的id--允许创建子文件夹
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
                # 确保看板文件夹名存在
                if dashboard_archive_name:
                    # 不存在父ID--一级文件夹--直接将文件夹名写入数据库中，不需要校验名称是否重复
                    # 默认第一次创建的文件夹 创建人和修改人一样
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

@bi.route("/archives/<int:id>",methods=["PUT"])
def update_archive_by_id(id):
    '''修改文件夹信息'''
    if request.method == 'PUT':
        # 最基础修改--还未判断新添加用户组的修改情况
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

            # 文件夹信息只有自己能修改，其他人无权修改
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

@bi.route("/archives/<int:id>",methods=["DELETE"])
def delete_archive_by_id(id):
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

@bi.route("/charts/",methods=["POST"])
def add_chart():
    # 添加图表接口
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
        # dmp_data_table_id、query_string、chart_data、chart_type、params都不可为空 ?
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

@bi.route("/charts/<int:id>",methods=["PUT"])
def update_charts_by_id(id):
    # 修改图表
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

            # 图表信息只能自己修改，其他人无权修改
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

@bi.route("/charts/<int:id>",methods=["DELETE"])
def delete_charts_by_id(id):
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
