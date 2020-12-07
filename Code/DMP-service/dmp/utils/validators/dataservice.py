#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 CatMan <garfield_lv@163.com>
#
# Distributed under terms of the MIT license.

"""

"""
from validator import Validator, StringField, IntegerField, EnumField


class Add_dataservice_validator(Validator):
    source_dmp_data_table_id = IntegerField(min_value=1, required=True)
    request_method = EnumField(choices=[1,2], required=True)
    state = EnumField(choices=[0, 1], required=False)
    data_service_name = StringField(max_length=64, required=True)
    api_path = StringField(max_length=64, required=False)
    query_sql = StringField(max_length=65535, required=False)

class Update_dataservice_validator(Validator):
    source_dmp_data_table_id = IntegerField(min_value=1, required=False)
    request_method = EnumField(choices=[1,2], required=False)
    state = EnumField(choices=[0, 1], required=False)
    data_service_name = StringField(max_length=64, required=False)
    api_path = StringField(max_length=64, required=False)
    query_sql = StringField(max_length=65535, required=False)

class Get_dataservice_validator(Validator):
    page_num = IntegerField(min_value=1,required=False)
    pagesize = IntegerField(min_value=1,required=False)
    data_service_name = StringField(max_length=64,required=False)
