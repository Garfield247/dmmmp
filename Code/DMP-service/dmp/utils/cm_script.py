#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/6/22
# @Author  : SHTD 


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/6/11
# @Author  : SHTD

import time
import datetime
import cm_client as cm
from cm_client.rest import ApiException


user = "admin"
password = "admin"
host = "192.168.3.140"
port = 7180
version = "v19"
api_url = "http://%s:%d/api/%s" % (host, port, version)


import cm_client
api_client = cm_client.ApiClient(api_url)
services_api_health = cm_client.ServicesResourceApi(api_client)
services_api_IO = cm_client.TimeSeriesResourceApi(api_client)

def get_model_health():
    try:
        import cm_client
        api_client = cm_client.ApiClient(api_url)
        services_api_health = cm_client.ServicesResourceApi(api_client)
        services = services_api_health.read_services("cluster")
        return [{"display_name":summary.display_name,"health_summary":summary.health_summary} for summary in services.items]
    except Exception as e:
        return str(e)

def get_disk_IO(time_interval):
    from_time = datetime.datetime.fromtimestamp(time.time() - int(time_interval))
    to_time = datetime.datetime.fromtimestamp(time.time())
    query = "select total_read_bytes_rate_across_disks, total_write_bytes_rate_across_disks where category = CLUSTER"
    res = services_api_IO.query_time_series(_from=from_time, query=query, to=to_time)
    return res

def get_network_IO(time_interval):
    from_time = datetime.datetime.fromtimestamp(time.time() - int(time_interval))
    to_time = datetime.datetime.fromtimestamp(time.time())
    query = "select total_bytes_receive_rate_across_network_interfaces, total_bytes_transmit_rate_across_network_interfaces where category = CLUSTER"
    res = services_api_IO.query_time_series(
        _from=from_time, query=query, to=to_time)
    return res

def get_cpu_usage(time_interval):
    from_time = datetime.datetime.fromtimestamp(time.time() - int(time_interval))
    to_time = datetime.datetime.fromtimestamp(time.time())
    query = "select cpu_percent_across_hosts where category = CLUSTER"
    res = services_api_IO.query_time_series(_from=from_time, query=query, to=to_time)
    return res

def get_hdfs_IO( time_interval):
    from_time = datetime.datetime.fromtimestamp(
        time.time() - int(time_interval))
    to_time = datetime.datetime.fromtimestamp(time.time())
    query = "select total_bytes_read_rate_across_datanodes, total_bytes_written_rate_across_datanodes where category = SERVICE and serviceType = HDFS"
    res = services_api_IO.query_time_series(
        _from=from_time, query=query, to=to_time)
    return res
