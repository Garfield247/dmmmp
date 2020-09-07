#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

from flask import Blueprint
from dmp.models import DataService, Users, UserDataService
from dmp.utils.engine import auto_connect
from dmp.extensions import limiter
from flask import Blueprint, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length
from dmp.models import DataService, Users, DataServiceParameter, DataTable
from dmp.utils import resp_hanlder

ds = Blueprint("ds", __name__)


@ds.route("/dataservices", methods=["GET"],
          defaults={"desc": {"interface_name": "查询多个数据服务", "is_permission": True, "permission_belong": 0}})
def get_data_services(desc):
    if request.method == 'GET':
        try:
            auth_token = request.headers.get("Authorization")
            user_id = Users.decode_auth_token(auth_token)
            if request.json:
                data_service_name = request.json.get("data_service_name", None)
                if data_service_name and len(data_service_name) > 50:
                    return resp_hanlder(code=101, msg="要进行检索的服务名称超长")
                page_num = request.json.get("page_num", 1)
                pagesize = request.json.get("pagesize", 10)
            else:
                page_num = 1
                pagesize = 10
                data_service_name = None
            results = DataService.query.filter_by(created_dmp_user_id=user_id)
            if data_service_name and len(data_service_name) > 0:
                results = results.filter(DataService.data_service_name.like('%' + data_service_name + '%'))
            results = results.limit(pagesize).offset((int(page_num) - 1) * int(pagesize))
            data = [d.__json__() for d in results]
            return resp_hanlder(result=data)
        except Exception as err:
            return resp_hanlder(code=999, error=err)


@ds.route("/dataservices/<int:id>", methods=["GET"],
          defaults={"desc": {"interface_name": "获取单一数据服务", "is_permission": True, "permission_belong": 0}})
def get_data_service_by_id(id, desc):
    if request.method == 'GET':
        try:
            auth_token = request.headers.get("Authorization")
            user_id = Users.decode_auth_token(auth_token)
            data_services = DataService.get(id)
            if data_services:
                create_user_id = data_services.created_dmp_user_id
                '''判断数据服务是否属于当前用户'''
                if create_user_id != user_id:
                    return resp_hanlder(code=301)
                parameters = [d.__json__() for d in DataServiceParameter.query.filter_by(dmp_data_service_id=id)]
                result = data_services.__json__()
                result['parameters'] = parameters
                return resp_hanlder(result=result)
            else:
                return resp_hanlder(code=7401, msg="数据服务不存在或在操作期间被删除")
        except Exception as err:
            return resp_hanlder(code=999, error=err)


@ds.route("/dataservices", methods=["POST"],
          defaults={"desc": {"interface_name": "添加数据服务", "is_permission": True, "permission_belong": 0}})
def add_data_services(desc):
    if request.method == 'POST':
        try:
            form = DataServiceForm(csrf_enabled=False)
            if not form.validate_on_submit():
                return resp_hanlder(code=101, err=form.errors)
            auth_token = request.headers.get("Authorization")
            user_id = Users.decode_auth_token(auth_token)
            data = request.json
            data_service_name = data.get("data_service_name")
            api_path = data.get("api_path")
            if DataService.exsit_data_service_by_apipath(apipath=api_path):
                return resp_hanlder(code=101, msg="API路径已存在")
            request_method = data.get("request_method")
            description = data.get("description")
            data_service = DataService(data_service_name=data_service_name,
                                       api_path=api_path,
                                       request_method=request_method,
                                       created_dmp_user_id=user_id,
                                       description=description)
            data_service.save()
            return resp_hanlder(result={"add_data_service": "complete!"})
        except Exception as err:
            return resp_hanlder(code=999, error=err)


@ds.route("/dataservices/<int:id>", methods=["PUT"],
          defaults={"desc": {"interface_name": "修改数据服务", "is_permission": True, "permission_belong": 0}})
def update_data_service_by_id(id, desc):
    if request.method == 'PUT':
        try:
            auth_token = request.headers.get("Authorization")
            current_user_id = Users.decode_auth_token(auth_token)
            if not current_user_id or not id:
                return resp_hanlder(code=201)
            if DataService.exist_item_by_id(id):
                data_service = DataService.get(id)
                if current_user_id == data_service.created_dmp_user_id:
                    data = request.json
                    if "data_service_name" in data.keys():
                        data_service.data_service_name = data.get("data_service_name")
                    if "api_path" in data.keys():
                        api_path = data.get("api_path")
                        if DataService.exsit_data_service_by_apipath(apipath=api_path):
                            item_api_path = data_service.api_path
                            if item_api_path == api_path:
                                data_service.api_path = api_path
                            else:
                                return resp_hanlder(code=101, msg="API路径已存在")
                        else:
                            data_service.api_path = api_path
                    if "request_method" in data.keys():
                        data_service.request_method = data.get("request_method")
                    if "description" in data.keys():
                        data_service.description = data.get("description")
                    if "source_dmp_data_table_id" in data.keys():
                        data_service.source_dmp_data_table_id = data.get("source_dmp_data_table_id")
                        if not DataTable.exist_item_by_id(data.get("source_dmp_data_table_id")):
                            return resp_hanlder(code=101, msg="源数据表不存在")
                    if "query_sql" in data.keys():
                        data_service.query_sql = data.get("query_sql")
                    if "query_params" in data.keys():
                        data_service.query_params = data.get("query_params")
                    if "state" in data.keys():
                        data_service.state = data.get("state")
                    data_service.changed_dmp_user_id = current_user_id
                    form = DataServiceForm(csrf_enabled=False)
                    if not form.validate_on_submit():
                        return resp_hanlder(code=101, err=form.errors)
                    data_service.put()
                    return resp_hanlder(result={"update_data_service": "complete!"})
                else:
                    return resp_hanlder(code=301)
            else:
                return resp_hanlder(code=7401, msg="数据服务不存在或在操作期间被删除")
        except Exception as err:
            return resp_hanlder(code=999, error=err)


@ds.route("/dataservices/<int:id>", methods=["DELETE"],
          defaults={"desc": {"interface_name": "删除数据服务", "is_permission": True, "permission_belong": 0}})
def delete_data_service_by_id(id, desc):
    if request.method == 'DELETE':
        try:
            if id:
                if DataService.exist_item_by_id(id):
                    item = DataService.get(id)
                    auth_token = request.headers.get("Authorization")
                    user_id = Users.decode_auth_token(auth_token)
                    if user_id == item.created_dmp_user_id:
                        item.delete()
                        return resp_hanlder(result={"delete_data_service": "success"})
                    else:
                        return resp_hanlder(code=301)
                else:
                    return resp_hanlder(code=7401, msg="数据服务不存在或在操作期间被删除")
            else:
                return resp_hanlder(code=101)
        except Exception as err:
            return resp_hanlder(code=999, error=err)


@ds.route("/ds_parameters", methods=["POST"],
          defaults={"desc": {"interface_name": "添加数据服务参数", "is_permission": True, "permission_belong": 0}})
def add_ds_parameters(desc):
    if request.method == 'POST':
        try:
            auth_token = request.headers.get("Authorization")
            user_id = Users.decode_auth_token(auth_token)
            if user_id:
                data = request.json
                data_service_id = data.get("dmp_data_service_id")
                if DataService.exist_item_by_id(data_service_id):
                    data_service = DataService.get(data_service_id)
                    create_user_id = data_service.created_dmp_user_id
                    if user_id != create_user_id:
                        return resp_hanlder(code=301)
                    else:
                        parameters = data.get("parameters")
                        data_service_parameters = []
                        for item in parameters:
                            form = DataServiceParameterForm(csrf_enabled=False, data=item)
                            if not form.validate_on_submit():
                                return resp_hanlder(code=201, err=form.errors)
                            parameter_name = item.get("parameter_name")
                            parameter_type = item.get("type")
                            required_parameter = item.get("required_parameter")
                            description = item.get("description")
                            data_service_parameter = DataServiceParameter(dmp_data_service_id=data_service_id,
                                                                          parameter_name=parameter_name,
                                                                          type=parameter_type,
                                                                          required_parameter=required_parameter,
                                                                          description=description)
                            data_service_parameters.append(data_service_parameter)
                        data_service_parameter.save_bulk(data_service_parameters)
                        return resp_hanlder(result={"add_data_service_parameter": "success"})
                else:
                    return resp_hanlder(code=7401, msg="数据服务不存在或在操作期间被删除")
            else:
                return resp_hanlder(code=301)
        except Exception as err:
            return resp_hanlder(code=999, error=err)


@ds.route("/ds_parameters/<int:id>", methods=["PUT"],
          defaults={"desc": {"interface_name": "修改数据服务参数", "is_permission": True, "permission_belong": 0}})
def update_ds_parameters(id, desc):
    if request.method == 'PUT':
        try:
            auth_token = request.headers.get("Authorization")
            user_id = Users.decode_auth_token(auth_token)
            if user_id:
                data = request.json
                data_service_id = data.get("dmp_data_service_id")
                if DataService.exist_item_by_id(data_service_id):
                    data_service = DataService.get(data_service_id)
                    create_user_id = data_service.created_dmp_user_id
                    if user_id != create_user_id:
                        return resp_hanlder(code=301)
                    else:
                        if not DataServiceParameter.exist_item_by_id(id):
                            return resp_hanlder(code=7501, msg="数据服务参数不存在或在操作期间被删除")
                        data_service_parameter = DataServiceParameter.get(id)
                        if "parameter_name" in data.keys():
                            data_service_parameter.parameter_name = data.get("parameter_name")
                        if "type" in data.keys():
                            data_service_parameter.type = data.get("type")
                        if "required_parameter" in data.keys():
                            data_service_parameter.required_parameter = data.get("required_parameter")
                        if "description" in data.keys():
                            data_service_parameter.description = data.get("description")
                        form = DataServiceParameterForm(csrf_enabled=False)
                        if not form.validate_on_submit():
                            return resp_hanlder(code=101, err=form.errors)
                        data_service_parameter.put()
                        return resp_hanlder(result={"put_data_service_parameter": "success"})
                else:
                    return resp_hanlder(code=7401, msg="数据服务不存在或在操作期间被删除")
            else:
                return resp_hanlder(code=301)
        except Exception as err:
            return resp_hanlder(code=999, err=err)


def parse_query_params(request_params, dataservice):
    legal = True
    query_params = {}
    missing = []
    dsparams = crrent_data_sevice.params
    for dsp in dsparams:
        p_name = dsp.get("parameter_name")
        p_required = dsp.get("required")
        value = request_params.get(p_name, None)
        if p_required == True and value != None:
            query_params[p_name] = value
        elif p_required == False and value != None:
            query_params[p_name] = value
        elif p_required == True and value == None:
            missing.append(p_name)
            legal = False
    if legal:
        return None, query_params
    else:
        return missing, None


def format_sql(query_sql_tmp, query_params):
    for param_name, value in query_params.items():
        query_sql_tmp = query_sql_tmp.replace(
            "{%s}" % str(param_name), str(value))

    return query_sql_tmp


@ds.route("/api/<path:api>", methods=["GET"])
@limiter.limit("1/second")
def get_data_by_data_service():
    request_params = request.json
    code = 100
    msg = None
    result = None
    secret_key = request_params.get("secret_key", None)
    if secret_key:
        user_id = Users.encode_auth_token(secret_key)
        if DataService.exsit_data_service_by_apipath(api):
            current_data_sevice = DataService.query.filter_by(
                api_path=api).first()
            if current_data_sevice.state:
                dataservice_log = UserDataService(
                    dmp_user_id=user_id,
                    dmp_data_service_id=current_data_sevice.id,
                )
                dataservice_log.save()
                missing, query_params = parse_query_params(
                    request_params, current_data_sevice)
                if missing == None:
                    query_sql_tmp = current_data_sevice.query_sql
                    source_dmp_data_table_id = current_data_sevice.source_dmp_data_table_id
                    if query_sql_tmp and source_dmp_data_table_id:
                        page_num = request_params.get(page_num, 1)
                        query_sql = format_sql(query_sql_tmp, query_params)
                        conn = auto_connect(table_id=source_dmp_data_table_id)
                        res, data = conn.exec_query_sql(query_sql)
                        if res:
                            result = data
                        else:
                            code = 8107
                    else:
                        code = 8106
                else:
                    code = 8105
                    msg = "缺少%d个必要参数：%s" % (len(missing), ",".join(missing))
            else:
                code = 8108
        else:
            code = 8104
    else:
        code = 8101
    return resp_hanlder(code=code, msg=msg, result=result)


class DataServiceForm(FlaskForm):
    data_service_name = StringField("data_service_name",
                                    validators=[DataRequired(message="API名称不能为空"),
                                                Length(max=50, message="API名称长度不能超过50!")])
    api_path = StringField("api_path",
                           validators=[DataRequired(message="API路径不能为空"), Length(max=255, message="API路径长度不能超过255!")])
    request_method = SelectField("request_method", choices={1})
    description = StringField("description", validators=[Length(max=400, message="API描述长度不能超过400")])


class DataServiceParameterForm(FlaskForm):
    parameter_name = StringField("parameter_name",
                                 validators=[DataRequired(message="参数名不能为空"),
                                             Length(max=100, message="参数名长度不能超过100!")])
    type = StringField("type", validators=[DataRequired(), Length(max=50, message="字段类型长度不能超过50!")])
    required_parameter = SelectField("required_parameter", choices={0, 1})
    description = StringField("description", validators=[Length(max=400, message="简介长度不能超过400")])
