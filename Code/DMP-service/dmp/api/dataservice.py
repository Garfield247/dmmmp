#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

from flask import Blueprint
from dmp.utils.engine import auto_connect
from dmp.extensions import limiter
from flask import Blueprint, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length
from dmp.models import DataService, Users, DataServiceParameter, DataTable
from dmp.models import UserDataService
from dmp.utils import resp_hanlder
# from dmp.utils.validators.dataservice import DataServiceForm, DataServiceParameterForm
from dmp.utils.validators.dataservice import Add_dataservice_validator,Update_dataservice_validator,Get_dataservice_validator


ds = Blueprint("ds", __name__)


@ds.route("/dataservices", methods=["GET"],
          defaults={"desc": {"interface_name": "查询多个数据服务", "is_permission": True, "permission_belong": 0}})
def get_data_services(desc):
    """
    查询多个数据服务
    ---
    tags:
      - DataService
    parameters:
      - name: data_service_name
        in: json
        type: string
        required: false
        description: 要进行检索的服务名
      - name: page_num
        in: json
        type: string
        required: int
        description: 页码
        default: '1'
      - name: pagesize
        in: json
        type: string
        required: int
        description: 单页数量
        default: '10'
    definitions:
      DataService:
        type: object
        properties:
            id:
              type: integer
              description: 数据服务ID
            data_service_name:
              type: string
              description: 数据服务名称
            request_method:
              type: integer
              description: 请求方法1get2post
            source_dmp_data_table_id:
              type: integer
              description: 源数据表ID
            projection:
              type: string
              description: 预选字段
            state:
              type: integer
              description: 是否启用
            description:
              type: string
              description: 数据服务简介
            created_on:
              type: string
              description: 创建时间
            changed_on:
              type: string
              description: 最后修改时间
            created_dmp_user_id:
              type: integer
              description: 创建人ID
            changed_dmp_user_id:
              type: integer
              description: 最后修改人ID
            created_dmp_user_name:
              type: string
              description: 创建人名称
            changed_dmp_user_name:
              type: string
              description: 最后修改人名称
      DataServiceParameter:
        type: object
        properties:
            id:
              type: integer
              description: 数据服务参数ID
            parameter_name:
              type: string
              description: 数据服务参数名称
            type:
              type: integer
              description: 数据类型
            source_dmp_data_table_id:
              type: integer
              description: 源数据表ID
            required_parameter:
              type: integer
              description: 是否必填
            description:
              type: string
              description: 数据服务简介
      DataServiceItems:
          properties:
            results:
              type: array
              items:
                $ref: '#/definitions/DataService'
      DataServiceParameterItem:
          properties:
            id:
              type: integer
              description: 数据服务ID
            data_service_name:
              type: string
              description: 数据服务名称
            request_method:
              type: integer
              description: 请求方法1get2post
            source_dmp_data_table_id:
              type: integer
              description: 源数据表ID
            projection:
              type: string
              description: 预选字段
            state:
              type: integer
              description: 是否启用
            description:
              type: string
              description: 数据服务简介
            created_on:
              type: string
              description: 创建时间
            changed_on:
              type: string
              description: 最后修改时间
            created_dmp_user_id:
              type: integer
              description: 创建人ID
            changed_dmp_user_id:
              type: integer
              description: 最后修改人ID
            created_dmp_user_name:
              type: string
              description: 创建人名称
            changed_dmp_user_name:
              type: string
              description: 最后修改人名称
            parameters:
              type: array
              $ref: '#/definitions/DataServiceParameter'
      DataServiceParameterItems:
          properties:
            results:
              type: array
              items:
                $ref: '#/definitions/DataServiceParameterItem'
    responses:
      500:
        description: Error The language is not awesome!
      0:
        description: 查询数据服务信息
        schema:
          $ref: '#/definitions/DataServiceItems'
    """
    if request.method == 'GET':
        try:
            auth_token = request.headers.get("Authorization")
            current_user_id = Users.decode_auth_token(auth_token)
            request_json = request.json if request.json else {}
            valid = Get_dataservice_validator(request_json)
            if not valid.is_valid():
                return resp_hanlder(code=201, msg=valid.str_errors)
            data_service_name = request.json.get("data_service_name", None)
            page_num = request.json.get("page_num", 1)
            pagesize = request.json.get("pagesize", 10)
            filters = {
                DataService.created_dmp_user_id == current_user_id,
            }
            if data_service_name != None:
                filters.add(DataService.data_service_name.like("%"+data_service_name+"%"))
            data_services_query = DataService.query.filter(*filters)
            data_count = data_services_query.count()
            data_services = data_services_query.limit(pagesize).offset((int(page_num) - 1) * int(pagesize))
            data = [d.__json__() for d in data_services]
            results = {
                'data': data,
                'page_num': page_num,
                'pagesize': pagesize,
                'data_count': data_count
            }
            return resp_hanlder(result=results)
        except Exception as err:
            raise err
            return resp_hanlder(code=999, error=err)


@ds.route("/dataservices/<int:id>", methods=["GET"],
          defaults={"desc": {"interface_name": "获取单一数据服务", "is_permission": True, "permission_belong": 0}})
def get_data_service_by_id(id, desc):
    """
    获取单一数据服务
    ---
    tags:
      - DataService
    parameters:
      - name: id
        in: path
        type: int
        required: true
        description: URL参数要获取的数据服务内容的ID
    responses:
      500:
        description: Error The language is not awesome!
      0:
        description: 查询单一数据服务信息
        schema:
           $ref: '#/definitions/DataServiceParameterItems'

    """
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
    """
    添加数据服务
    ---
    tags:
      - DataService
    parameters:
      - name: data_service_name
        in: json
        type: string
        required: true
        description: 数据服务名称
      - name: api_path
        in: json
        type: string
        required: true
        description: 数据服务接口
      - name: request_method
        in: json
        type: integer
        required: true
        description: 请求方法1get2post
      - name: description
        in: json
        type: string
        required: false
        description: 简介
    responses:
      500:
        description: Error The language is not awesome!
      0:
        msg: 'ok'
    """
    if request.method == 'POST':
        try:
            auth_token = request.headers.get("Authorization")
            user_id = Users.decode_auth_token(auth_token)
            request_json = request.json
            valid = Add_dataservice_validator(request_json)
            if not valid.is_valid():
                return resp_hanlder(code=201, msg=valid.str_errors)
            data_service_name = data.get("data_service_name")
            api_path = data.get("api_path")
            if DataService.exsit_data_service_by_apipath(apipath=api_path):
                return resp_hanlder(code=101, msg="API路径已存在")
            request_method = data.get("request_method")
            description = data.get("description")
            source_dmp_data_table_id = request_json.get("source_dmp_data_table_id")
            data_service = DataService(data_service_name=data_service_name,
                                       api_path=api_path,
                                       source_dmp_data_table_id=source_dmp_data_table_id,
                                       request_method=request_method,
                                       created_dmp_user_id=user_id,
                                       changed_dmp_user_id=user_id,
                                       description=description)
            data_service.save()
            return resp_hanlder(result={"add_data_service": "complete!", "id": data_service.id})
        except Exception as err:
            return resp_hanlder(code=999, error=err)


@ds.route("/dataservices/<int:id>", methods=["PUT"],
          defaults={"desc": {"interface_name": "修改数据服务", "is_permission": True, "permission_belong": 0}})
def update_data_service_by_id(id, desc):
    """
    修改数据服务
    ---
    tags:
      - DataService
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: URL参数，要修改的数据服务的ID
      - name: data_service_name
        in: json
        type: string
        required: false
        description: 数据服务名称
      - name: api_path
        in: json
        type: string
        required: false
        description: 数据服务接口
      - name: request_method
        in: json
        type: integer
        required: false
        description: 请求方法1get2post
      - name: description
        in: json
        type: string
        required: false
        description: 简介
      - name: source_dmp_data_table_id
        in: json
        type: integer
        required: false
        description: 源数据表ID
      - name: query_sql
        in: json
        type: string
        required: false
        description: 查询语句（mysql）
      - name: query_params
        in: json
        type: integer
        required: false
        description: 查询参数（mongodb）
      - name: state
        in: json
        type: integer
        required: false
        description: 是否启用
    responses:
      500:
        description: Error The language is not awesome!
      0:
        msg: 'ok'
    """
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
                    valid = Update_dataservice_validator(data)
                    if not valid.is_valid():
                        return resp_hanlder(code=201,msg=valid.str_errors)
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
    """
    删除数据服务
    ---
    tags:
      - DataService
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: URL参数，要删除的数据服务的ID
    responses:
      500:
        description: Error The language is not awesome!
      0:
        msg: 'ok'
    """
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
    """
    添加数据服务参数
    ---
    tags:
      - DataService
    parameters:
      - name: dmp_data_service_id
        in: json
        type: integer
        required: true
        description: 数据服务ID
      - name: parameter_name
        in: json
        type: string
        required: true
        description: 参数名
      - name: type
        in: json
        type: string
        required: true
        description: 字段类型
      - name: required_parameter
        in: json
        type: integer
        required: false
        description: 是否是必填项
      - name: description
        in: json
        type: string
        required: false
        description: 简介
    responses:
      500:
        description: Error The language is not awesome!
      0:
        msg: 'ok'
    """
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
                        if parameters is None or len(parameters) == 0:
                            return resp_hanlder(result={"add_data_service_parameter": "success"})
                        data_service_parameters = []
                        for item in parameters:
                            # form = DataServiceParameterForm(csrf_enabled=False, data=item)
                            # if not form.validate_on_submit():
                                # return resp_hanlder(code=201, err=form.errors)
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
    """
    修改数据服务参数
    ---
    tags:
      - DataService
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: 数据服务参数ID
      - name: dmp_data_service_id
        in: json
        type: integer
        required: true
        description: 数据服务ID
      - name: parameter_name
        in: json
        type: string
        required: false
        description: 参数名
      - name: type
        in: json
        type: string
        required: false
        description: 字段类型
      - name: required_parameter
        in: json
        type: integer
        required: false
        description: 是否是必填项
      - name: description
        in: json
        type: string
        required: false
        description: 简介
    responses:
      500:
        description: Error The language is not awesome!
      0:
        msg: 'ok'
    """
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
    dsparams = dataservice.params
    print(dsparams)
    if dsparams:
        if len(dsparams)>0:
            for dsp in dsparams:
                p_name = dsp.get("parameter_name")
                p_required = dsp.get("required_parameter")
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
        else:
            return None,None
    else:
        return None,None


def format_sql(query_sql_tmp, query_params):

    for param_name, value in query_params.items():
        value_ = value
        if type(value) == int or type(value) == float:
            value_ = str(value)
        elif type(value) == str:
            value_ = "'%s'"%(value)
        elif type(value) == list:
            vs = []
            for v in value:
                if type(v) == int or type(v) == float:
                    vs.append(str(v))
                elif type(v) == str:
                    vs.append( "'%s'"%(v))
                else:
                    raise Exception("参数值不合法")
            value_ = ",".join(vs)
        else:
            raise Exception("参数值不合法")
        query_sql_tmp = query_sql_tmp.replace("{%s}" % str(param_name), "%s"%value_)

    return query_sql_tmp


@ds.route("/api/<path:api>", methods=["GET"])
@limiter.limit("1/second")
def get_data_by_data_service(api):
    """
    数据服务调用

    ---
    tags:
      - DataService
    parameters:
      - name: api
        type: string
        required: true
        description: 数据接口路径
      - name: secret_key
        type: string
        required: true
        description: 密钥
      - name: page_num
        type: int
        required: true
        description: 数据页码
      - name: 其他参数
        type: string
        required: false
        description: 数据服务的筛选参数
    responses:
      0:
        description: 正常响应
	"""
    try:
        api = str(api)
        print(api)
        request_params = request.json
        code = 100
        msg = None
        result = None
        secret_key = request_params.get("secret_key", None)
        if secret_key:
            user_id = Users.encode_auth_token(secret_key)
        else:
            code = 8101
            msg = "缺少秘钥或秘钥已失效"
            return resp_hanlder(code=code, msg=msg, result=result)

        if DataService.exsit_data_service_by_apipath(api):
            current_data_sevice = DataService.query.filter_by(api_path=api).first()
        else:
            code = 8104
            msg = "未匹配到改数据服务"
            return resp_hanlder(code=code, msg=msg, result=result)
        if current_data_sevice.state:
            # dataservice_log = UserDataService(
                # dmp_user_id=user_id,
                # dmp_data_service_id=current_data_sevice.id,
            # )
            # dataservice_log.save()
            db_type = current_data_sevice.database_type
            missing, query_params = parse_query_params(request_params, current_data_sevice)
        else:
            code = 8108
            msg = "当前数据服务未开启"
            return resp_hanlder(code=code, msg=msg, result=result)
        if missing == None:
            source_dmp_data_table_id = current_data_sevice.source_dmp_data_table_id
        else:
            code = 8105
            msg = "缺少%d个必要参数：%s" % (len(missing), ",".join(missing))
            return resp_hanlder(code=code, msg=msg, result=result)
        if source_dmp_data_table_id:
            page_num = request_params.get("page_num", 1)
            page_size = request_params.get("page_size", 100)
            conn = auto_connect(table_id=source_dmp_data_table_id)
            qp = {}
            if db_type in [1, 2]:
                query_sql_tmp = current_data_sevice.query_sql
                query_sql = format_sql(query_sql_tmp, query_params) if  query_params else query_sql_tmp
                qp["sql"] = query_sql
                print(qp)
                data = conn.exec_query(**qp)
                result = data
                return resp_hanlder(code=code, msg=msg, result=result)
            elif db_type == 3:
                query_sql_tmp = current_data_sevice.query_params
                query_sql = eval(query_sql_tmp)
                query_sql[filter] = query_params
                qp = query_sql
                print(qp)
                data = conn.exec_query(**qp)
                result = data
                return resp_hanlder(code=code, msg=msg, result=result)
            else:
                code = 8107
                msg = "源数据库异常"
                return resp_hanlder(code=code, msg=msg, result=result)

        else:
            msg = "源数据库异常"
            code = 8106
            return resp_hanlder(code=code, msg=msg, result=result)
    except Exception as err:
        # raise err
        return resp_hanlder(code=999, msg=str(err))
