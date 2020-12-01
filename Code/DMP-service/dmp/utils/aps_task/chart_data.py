#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

def update_chart_data(chart_id):
    import json
    from dmp import app
    with app.app_context():
        from flask import current_app
        from dmp.models import Chart
        from dmp.utils.engine import auto_connect
        if Chart.exist_item_by_id(chart_id):
            current_chart = Chart.get(chart_id)
            data_table_id = current_chart.dmp_data_table_id
            query_string = current_chart.query_string
            conn = auto_connect(table_id=data_table_id)
            if current_chart.dmp_data_table.dmp_database_type in [1, 2, 4]:
                request_json = {
                    "sql":query_string.get("sql")
                        }
                _data = conn.exec_query(**request_json)
                if type(_data) ==  list:
                    field = query_string.get("fields")

                    current_chart.chart_data = [dict(zip(field , d)) for d in _data]
                    current_chart.put()
                return True,"OK"
        else:
            return False,"item not exist"



