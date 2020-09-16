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


class Get_dashboards_and_archives_validator(Validator):
    upper_dmp_dashboard_archive_id = IntegerField(min_value=1, required=False)
    is_owner = EnumField(choices=[True, False], required=True)
    state = EnumField(choices=[0, 1, 2], required=False)
    name = StringField(max_length=64, required=False)
