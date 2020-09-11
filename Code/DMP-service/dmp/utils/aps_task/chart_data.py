#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD
from dmp.models import Chart
from dmp.utils.engine import auto_connect

def update_chart_data(chart_id):
    if Chart.exist_item_by_id(chart_id):
        current_chart = Chart.get(chart_id)
        data_table_id = current_chart.dmp_data_table_id
        query_string = current_chart.query_string
        conn = auto_connect(table_id=data_table_id)
    else:
        return False,"item not exist"



