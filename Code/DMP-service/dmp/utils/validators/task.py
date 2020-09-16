
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


class Add_query_data_task_validator(Validator):
    chart_id = IntegerField(min_value=1, required=True)
    time_unit = EnumField(choices=["weeks","days","hours","mins","seconds"], required=True)
    time_value = IntegerField(min_value=1, required=True)

class Update_query_data_task_validator(Validator):
    time_unit = EnumField(choices=["weeks","days","hours","mins","seconds"], required=True)
    time_value = IntegerField(min_value=1, required=True)
