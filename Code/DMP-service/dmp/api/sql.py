#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/10/14
# @Author  : SHTD

import json
import datetime
from flask import Blueprint
from dmp.utils.engine import auto_connect
from flask import Blueprint, request
from sqlalchemy import tuple_
from dmp.utils import resp_hanlder
from dmp.utils.engine import auto_connect
from dmp.models import SavedQuery,Case,DataTable,Users
from dmp.utils.validators.sql import Get_queries_validator,Add_queries_validator, Update_queries_validator
from dmp.extensions import db


sql = Blueprint("sql", __name__)


@sql.route("/queries", methods=["GET"],defaults={"desc": {"interface_name": "获取多个保存的SQL", "is_permission": True, "permission_belong": 0}})
def get_queries(desc):

    """
    获取多个保存的SQL
    名称查询均支持模糊查询
    ---
    tags:
      - SQL
    parameters:
      - name: query_name
        in:
        type: string
        required: false
        description: 查询的名称，最长64字符
      - name: case_name
        in:
        type: string
        required: false
        description: 案例名称，最长64字符
      - name: table_name
        in:
        type: string
        required: false
        description: 数据表名称,最长64字符
      - name: start_time
        in:
        type: string
        required: false
        description: 开始时间,最长64字符,示例：2020-10-14 17:58:00
      - name: end_time
        in:
        type: string
        required: false
        description: 结束时间,最长64字符,格式同上
      - name: pagesize
        in:
        type: int
        required: false
        description: 一页数量，最小值为1
      - name: pagenum
        in:
        type: int
        required: false
        description: 页码，最小值为1
    responses:
      0:
        description: ok
    """

    auth_token = request.headers.get('Authorization')
    current_user_id = Users.decode_auth_token(auth_token)
    request_json = request.json if request.json else {}

    valid = Get_queries_validator(request_json)
    if not valid.is_valid():
        return resp_hanlder(code=201, msg=valid.str_errors)

    query_name = request_json.get("query_name")
    case_name = request_json.get("case_name")
    table_name = request_json.get("table_name")
    start_time = request_json.get("start_time")
    end_time = request_json.get("end_time", str(datetime.datetime.now()))

    pagesize = request_json.get("pagesize", 10)
    pagenum = request_json.get("pagenum", 1)

    queries_filters = {
        SavedQuery.created_dmp_user_id == current_user_id
            }
    if query_name:
        queries_filters.add(SavedQuery.query_name.like("%"+query_name+"%"))
    if case_name:
        queries_filters.add(tuple_(SavedQuery.dmp_data_table_id).in_( db.session.query(DataTable.id).filter(tuple_(DataTable.dmp_case_id).in_(db.session.query(Case.id).filter(Case.dmp_case_name.like("%"+case_name+"%")).all())).all() ))
    if table_name:
        queries_filters.add(tuple_(SavedQuery.dmp_data_table_id).in_(db.session.query(DataTable.id).filter(DataTable.dmp_data_table_name.like("%"+table_name+"%")).all()))
    if start_time and end_time:
        queries_filters.add(SavedQuery.changed_on.between(start_time,end_time))

    queries_query = SavedQuery.query.filter(*queries_filters)
    count = queries_query.count()
    queries_objs = queries_query.offset((pagenum-1)*pagesize).limit(pagesize)
    queries_data = [q.__json__() for q in queries_objs]
    result = {
        "data":queries_data,
        "pagenum":pagenum,
        "pagesize":pagesize,
        "count":count
    }
    return resp_hanlder(code=0,result = result)

@sql.route("/queries/<int:query_id>", methods=["GET"],defaults={"desc": {"interface_name": "根据ID获取保存的SQL", "is_permission": True, "permission_belong": 0}})
def get_queries_by_id(desc, query_id):

    """
    根据ID获取保存的SQL

    ---
    tags:
      - SQL
    parameters:
      - name: query_id
        in:
        type: int
        required: ture
        description: 查询的ID
    responses:
      0:
        description: ok
    """
    auth_token = request.headers.get('Authorization')
    current_user_id = Users.decode_auth_token(auth_token)
    if SavedQuery.exist_item_by_id(query_id):
        query_obj =  SavedQuery.get(query_id)
        if query_obj.created_dmp_user_id == current_user_id:
            query_info = query_obj.__json__()
            result = {
                "data":query_info
            }
            return resp_hanlder(code=0, result=result)
        else:
            return resp_hanlder(code=999, msg="非改查询的所有者，无权查看")
    else:
        return resp_hanlder(code=999, msg="查询不存在或已被删除")


@sql.route("/queries", methods=["POST"],defaults={"desc": {"interface_name": "保存SQL", "is_permission": True, "permission_belong": 0}})
def add_queries(desc):

    """
    保存SQL

    ---
    tags:
      - SQL
    parameters:
      - name: query_name
        in:
        type: string
        required: true
        description: 查询的名称，最长64字符
      - name: query_sql
        in:
        type: string
        required: true
        description: 查询语句，最长65535字符
      - name: description
        in:
        type: string
        required: false
        description: 查询的简介，最长512字符
      - name: dmp_case_id
        in:
        type: int
        required: true
        description: 原数据案例ID
      - name: dmp_data_table_id
        in:
        type: int
        required: true
        description: 原数据表ID
    responses:
      0:
        description: OK
    """
    auth_token = request.headers.get('Authorization')
    current_user_id = Users.decode_auth_token(auth_token)
    request_json = request.json if request.json else {}

    valid = Add_queries_validator(request_json)
    if not valid.is_valid():
        return resp_hanlder(code=201, msg=valid.str_errors)
    new_queries = SavedQuery(
        query_name = request_json.get("query_name"),
        query_sql = request_json.get("query_sql"),
        description = request_json.get("description"),
        dmp_data_table_id = request_json.get("dmp_data_table_id"),
        dmp_case_id = request_json.get("dmp_case_id"),
        created_dmp_user_id = current_user_id,
        changed_dmp_user_id = current_user_id,
        )
    new_queries.save()
    return resp_hanlder(code=0,result=new_queries.__json__())

@sql.route("/queries/<int:query_id>", methods=["PUT"],defaults={"desc": {"interface_name": "更新保存的SQL", "is_permission": True, "permission_belong": 0}})
def update_queries_by_id(desc,query_id):

    """
    更新保存的SQL

    ---
    tags:
      - SQL
    parameters:
      - name: query_id
        in:
        type: int
        required: false
        description: 要进行修改的查询ID
      - name: query_name
        in:
        type: string
        required: false
        description: 查询的名称，最长64字符
      - name: query_sql
        in:
        type: string
        required: true
        description: 查询语句，最长65535字符
      - name: description
        in:
        type: string
        required: false
        description: 查询的简介，最长512字符
      - name: dmp_case_id
        in:
        type: int
        required: false
        description: 原数据案例ID
      - name: dmp_data_table_id
        in:
        type: int
        required: false
        description: 原数据表ID
    responses:
      0:
        description: OK
    """
    auth_token = request.headers.get('Authorization')
    current_user_id = Users.decode_auth_token(auth_token)
    request_json = request.json if request.json else {}
    print(request_json)
    valid = Update_queries_validator(request_json)
    if not valid.is_valid():
        return resp_hanlder(code=201, msg=valid.str_errors)
    if SavedQuery.exist_item_by_id(query_id):
        current_queries = SavedQuery.get(query_id)
        if current_queries.created_dmp_user_id == current_user_id:
            if request_json.get("query_name"):
                current_queries.query_name = request_json.get("query_name")
            if request_json.get("query_sql"):
                current_queries.query_sql = request_json.get("query_sql")
            if request_json.get("description"):
                current_queries.description = request_json.get("description")
            if request_json.get("dmp_data_table_id"):
                current_queries.dmp_data_table_id = request_json.get("dmp_data_table_id")
            if request_json.get("dmp_case_id"):
                current_queries.dmp_case_id = request_json.get("dmp_case_id")
            current_queries.changed_dmp_user_id = current_user_id
            current_queries.put()
            return resp_hanlder(code=0,result="OK")
        else:
            return resp_hanlder(code=999, msg="您不是该查询的所有者,无权修改本查询")
    else:
        return resp_hanlder(code=999, msg="该查询不存在或已被删除")

@sql.route("/queries/<int:query_id>", methods=["DELETE"],defaults={"desc": {"interface_name": "删除保存的SQL", "is_permission": True, "permission_belong": 0}})
def del_queries_by_id(desc,query_id):

    """
    删除保存的SQL

    ---
    tags:
      - SQL
    parameters:
      - name: query_id
        in:
        type: int
        required: true
        description: 要删除的查询的ID
    responses:
      o:
        description: ok
    """
    auth_token = request.headers.get('Authorization')
    current_user_id = Users.decode_auth_token(auth_token)

    if SavedQuery.exist_item_by_id(query_id):
        current_queries = SavedQuery.get(query_id)
        if current_queries.created_dmp_user_id == current_user_id:
            current_queries.delete()
            return resp_hanlder(code=0,result="OK")
        else:
            return resp_hanlder(code=999, msg="您不是该查询的所有者,无权删除改查询")
    else:
        return resp_hanlder(code=999, msg="该查询不存在或已被删除")

@sql.route("/retrieve", methods=["GET"], defaults={"desc": {"interface_name": "SQL查询", "is_permission": True, "permission_belong": 0}})
def retrieve(desc):
    """
    SQL查询

    ---
    tags:
      - SQL
    parameters:
      - name: dmp_data_table_id
        in:
        type: int
        required: True
        description: 数据表ID
      - name: sql
        in:
        type: string
        required: false
        description: SQL 语句，mysql，hive ，kylin 必填
      - name: collection
        in:
        type: string
        required: false
        description: mongodb 参数  集合名(表名)

    responses:
      0:
        description: OK
    """
    request_json = request.json if request.json else {}
    data_table_id = request_json.get("dmp_data_table_id")
    if data_table_id:
        try:
            conn = auto_connect(table_id= data_table_id)
            result = conn.exec_query(**request_json)
            return resp_hanlder(code=0,result=result)
        except Exception as e:
            return resp_hanlder(code=999, msg=str(e))

    else:
        return resp_hanlder(code=999, msg="缺少dmp_data_table_id")


@sql.route("/chart_retrieve", methods=["GET"], defaults={"desc": {"interface_name": "图表查询", "is_permission": True, "permission_belong": 0}})
def chart_retrieve(desc):
    """
    图表查询

    ---
    tags:
      - SQL
    parameters:
      - name: dmp_data_table_id
        in:
        type: int
        required: True
        description: 数据表ID
      - name: dimension
        in:
        type: array
        required: True
        description: 维度，格式[{"name":"xxx"},{"name":"xxxxx"}]
      - name: measure
        in:
        type: array
        required: true
        description: 度量，格式[{"name":"xxx", "method":"count/sum/avg"},{......}]

    responses:
      0:
        description: OK
    """
    request_json = request.json if request.json else {}
    data_table_id = request_json.get("dmp_data_table_id")
    dimension = request_json.get("dimension")
    measure = request_json.get("measure")
    limit = request_json.get("limit")
    if data_table_id and DataTable.exist_item_by_id(data_table_id):
        data_table = DataTable.get(data_table_id)
        data_table_name = data_table.db_table_name
        db_type = data_table.dmp_database_type
        dimension_names = [d.get("name") for d in dimension]
        measure_names = [m.get("name") if m.get("method")==None else "%s(%s)"%(m.get("method"), m.get("name"))  for m in measure ]
        measure_names_methods = [m.get("name") if m.get("method")==None else "%s_%s"%( m.get("name"),m.get("method"))  for m in measure ]

        groupby =  bool(sum([True if m.get("method") else False for m in measure]))
        sql = "select {p1} from {p2} {p3} {p4}".format(p1=",".join(dimension_names+measure_names), p2=data_table_name, p3 = "group by "+",".join(dimension_names) if groupby else "" , p4 = ";" if db_type == 2 else "")
        request_json["sql"] = sql
        try:
            conn = auto_connect(table_id= data_table_id)
            _data = conn.exec_query(**request_json)
            func2f = lambda x:round(x,2) if type(x)==float else x
            if type(_data) ==  list or type(_data) == tuple:

                result = {}
                result["data"] = [dict(zip(dimension_names+measure_names_methods, map(func2f,d)) for d in _data]
                result["query_string"] = {"sql":sql, "fields":dimension_names+measure_names_methods}

                return resp_hanlder(code=0,result=result)
            else:
                return resp_hanlder(code=999,msg = "查询出错 你的查询SQl：%s"%sql)

        except Exception as e:
            return resp_hanlder(code=999, msg=str(e))

    else:
        return resp_hanlder(code=999, msg="缺少dmp_data_table_id")










@sql.route("/ds_retrieve", methods=["GET"], defaults={"desc": {"interface_name": "数据服务参数调试", "is_permission": True, "permission_belong": 0}})
def ds_retrieve(desc):
    """
    图表查询

    ---
    tags:
      - SQL
    parameters:
      - name: source_dmp_data_table_id
        in:
        type: int
        required: True
        description: 数据表ID
      - name: query_sql_tmp
        in:
        type: string
        required: True
        description: 要调试的查询语句
      - name: parameters
        in:
        type: dict
        required: true
        description: 参数，{"参数名":"参数值"}

    responses:
      0:
        description: OK
    """
    from .dataservice import format_sql
    try:
        request_json = request.json if request.json else {}
        data_table_id = request_json.get("source_dmp_data_table_id")
        query_sql_tmp = request_json.get("query_sql_tmp",None)
        parameters = request_json.get("parameters",{})
        code = 0
        if all([ data_table_id,query_sql_tmp ]):
            if DataTable.exist_item_by_id(data_table_id):
                current_data_table = DataTable.get(data_table_id)
            else:
                code=999
                msg="数据表不存在"
                return resp_hanlder(code=code,msg=msg)
            db_type = current_data_table.dmp_database_type
            qp = {}
            conn = auto_connect(table_id=data_table_id)
            if db_type in [1, 2]:
                query_sql = format_sql(query_sql_tmp, parameters) if  parameters else query_sql_tmp
                qp["sql"] = query_sql
                print(qp)
                data = conn.exec_query(**qp)
                result = data
                return resp_hanlder(code=code, result=result)
            elif db_type == 3:
                query_sql_tmp = current_data_sevice.query_params
                query_sql = eval(query_sql_tmp)
                query_sql[filter] = parameters
                qp = query_sql
                print(qp)
                data = conn.exec_query(**qp)
                result = data
                return resp_hanlder(code=code, result=result)
            else:
                code = 8107
                msg = "源数据库异常"
                return resp_hanlder(code=code, msg=msg)
        else:
            code = 201
            msg = "参数异常"
            return resp_hanlder(code=code, msg=msg)
    except Exception as err:
        code =999
        msg = str(err)
        return resp_hanlder(code=code, msg=msg)
