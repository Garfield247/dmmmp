#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/6/11
# @Author  : SHTD

import time
import datetime
import cm_client as cm
from cm_client.rest import ApiException

class CM_tools():
    user = "admin"
    password = "admin"
    host = "192.168.3.140"
    port = 7180
    version = "v19"
    api_url = "http://%s:%d/api/%s" % (host, port, version)

    def __init__(self):
        import cm_client as cm
        cm.configuration.username = "admin"
        cm.configuration.password = "admin"
        self.api_client = cm.ApiClient(self.api_url)
        self.services_api_health = cm.ServicesResourceApi(self.api_client)
        self.services_api_IO = cm.TimeSeriesResourceApi(self.api_client)

    def get_model_health(self):
        services = self.services_api_health.read_services("cluster")
        return [{"display_name":summary.display_name,"entity_status":summary.entity_status} for summary in services.items]

    def get_disk_IO(self,time_interval):
        from_time = datetime.datetime.fromtimestamp(time.time() - int(time_interval))
        to_time = datetime.datetime.fromtimestamp(time.time())
        query = "select total_read_bytes_rate_across_disks, total_write_bytes_rate_across_disks where category = CLUSTER"
        res = self.services_api_IO.query_time_series(_from=from_time, query=query, to=to_time).to_dict()
        return res

    def get_network_IO(self,time_interval):
        from_time = datetime.datetime.fromtimestamp(time.time() - int(time_interval))
        to_time = datetime.datetime.fromtimestamp(time.time())
        query = "select total_bytes_receive_rate_across_network_interfaces, total_bytes_transmit_rate_across_network_interfaces where category = CLUSTER"
        res = self.services_api_IO.query_time_series(_from=from_time, query=query, to=to_time).to_dict()
        return res

    def get_cpu_usage(self,time_interval):
        from_time = datetime.datetime.fromtimestamp(time.time() - int(time_interval))
        to_time = datetime.datetime.fromtimestamp(time.time())
        query = "select cpu_percent_across_hosts where category = CLUSTER"
        res = self.services_api_IO.query_time_series(_from=from_time, query=query, to=to_time).to_dict()
        return res

    def get_hdfs_IO(self, time_interval):
        from_time = datetime.datetime.fromtimestamp(
            time.time() - int(time_interval))
        to_time = datetime.datetime.fromtimestamp(time.time())
        query = "select total_bytes_read_rate_across_datanodes, total_bytes_written_rate_across_datanodes where category = SERVICE and serviceType = HDFS"
        res = self.services_api_IO.query_time_series(_from=from_time, query=query, to=to_time).to_dict()
        return res

    def get_hdfs_disk_usage(self, time_interval):
        from_time = datetime.datetime.fromtimestamp(
            time.time() - int(60))
        to_time = datetime.datetime.fromtimestamp(time.time())
        query = "select dfs_capacity, dfs_capacity_used, dfs_capacity_used_non_hdfs where entityName=hdfs"
        res = self.services_api_IO.query_time_series(_from=from_time, query=query, to=to_time).to_dict()

        res_ = [ {"metric_name":serie.get("metadata",{}).get("metric_name"),"value":serie.get("data",{})[0].get("value")} for serie in res.get("items",{})[0].get("time_series",[])]
        # print(res_)
        return res_