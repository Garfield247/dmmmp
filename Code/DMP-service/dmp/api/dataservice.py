#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

from flask import Blueprint
from dmp.models import DataService, Users, UserDataService
from dmp.utils import resp_hanlder
from dmp.utils.engine import auto_connect
from dmp.extensions import limiter


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
