#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/10/14
# @Author  : SHTD


from validator import Validator, StringField, IntegerField, EnumField


class Get_queries_validator(Validator):
    query_name = StringField(max_length=64, required=False)
    case_name = StringField(max_length=64, required=False)
    table_name = StringField(max_length=64, required=False)
    start_time = StringField(max_length=64, required=False)
    end_time = StringField(max_length=64, required=False)
    pagesize = IntegerField(min_value=1, required=False)
    pagenum = IntegerField(min_value=1, required=False)

class Add_queries_validator(Validator):
    query_name = StringField(max_length=64, required=True)
    query_sql = StringField(max_length=65535, required=True)
    description = StringField(max_length=512, required=False)
    dmp_case_id = IntegerField(min_value=1, required=True)
    dmp_data_table_id = IntegerField(min_value=1, required=True)

class Update_queries_validator(Validator):
    query_name = StringField(max_length=64, required=False)
    query_sql = StringField(max_length=65535, required=False)
    description = StringField(max_length=512, required=False)
    dmp_case_id = IntegerField(min_value=1, required=False)
    dmp_data_table_id = IntegerField(min_value=1, required=False)
