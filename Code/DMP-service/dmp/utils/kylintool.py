#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import os
import json
import base64
import requests
from flask import current_app


class KylinTool():

    def __init__(self, host, port, user, passwd):
        """
        初始化连接信息
        """
        self.headers = {
            "Authorization": self.build_authorization(user, passwd),
            "Content-Type": "application/json"
        }
        print(self.headers)
        self.url_prefix = "http://{host}:{port}/kylin/api/".format(
            host=host, port=port)

    def build_authorization(self, username, password):
        """
        创建认证信息
        """
        user_key = '%s:%s' % (username, password)
        b = base64.b64encode(user_key.encode())
        return "Basic "+str(b)[2:-1]

    def _get(self, api, params=None):
        """
        用于与Kylin restful API 交互的get请求封装
        """
        url = os.path.join(self.url_prefix, api)
        print(url)
        r = requests.get(url=url, headers=self.headers, params=params)
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception(r.json().get("msg"))

    def _post(self, api, params=None):
        """
        用于与Kylin restful API 交互的post请求封装
        """
        r = requests.post(url=self.url_prefix+api,
                          headers=self.headers, json=params)
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception(r.json().get("msg"))

    def _put(self, api, params=None):
        """
        用于与Kylin restful API 交互的put请求封装
        """
        r = requests.put(url=self.url_prefix+api,
                         headers=self.headers, json=params)
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception(r.json().get("msg"))

    def _del(self, api, params=None):
        """
        用于与Kylin restful API 交互的delete请求封装
        """
        r = requests.delete(url=self.url_prefix+api,
                            headers=self.headers, json=params)
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception(r.json().get("msg"))

    """
    code 代表响应状态码，后续注释会省略
    """

    """
    +++++++++++++++++++++++++++用户相关API+++++++++++++++++++++++++++++++++
    """

    def api_authentication(self):
        """
        当前用户状态
        参数：无
        返回值：
        userDetails ：定义的权限和当前用户的状态
        """
        result = self._post("authentication")
        return result

    """
    +++++++++++++++++++++++++++Query 查询相关API+++++++++++++++++++++++++++++++++
    """

    def api_query(self, sql, offset=0, limit=None, acceptPartial=True, project="DEFAULT"):
        """
        查询
        参数：
        sql - 必需 string sql语句的文本。
        offset - 可选 int  查询偏移量。如果在sql中设置了offset，则将被忽略。
        limit - 可选 int  查询限制。如果在sql中设置了limit，perPage将被忽略。
        acceptPartial - 可选 bool 是否接受部分结果，默认为“ false”。设置为“ false”以用于生产。
        project - 可选 string 项目执行查询。默认值为‘DEFAULT’。
        返回值：
        columnMetas-结果集的列元数据信息。
        results -结果数据集。
        cube-用于此查询的多维数据集。
        affectedRowCount -此sql语句影响的行数。
        isException-此响应是否为异常。
        ExceptionMessage-异常的消息内容。
        Duration -此查询的时间成本
        Partial -响应是否为部分结果。由request的acceptPartial决定。
        """
        params = {
            "sql": sql,
            "offset": offset,
            "limit": limit,
            "acceptPartial": acceptPartial,
            "project": project,
        }
        result = self._post("query", params=params)
        return result

    def api_prepare_query(self, sql, offset=0, limit=None, acceptPartial=False, project="DEFAULT"):
        """
        查询
        参数：
        sql - 必需 string sql语句的文本。
        offset - 可选 int  查询偏移量。如果在sql中设置了offset，则将被忽略。
        limit - 可选 int  查询限制。如果在sql中设置了limit，perPage将被忽略。
        acceptPartial - 可选 bool 是否接受部分结果，默认为“ false”。设置为“ false”以用于生产。
        project - 可选 string 项目执行查询。默认值为‘DEFAULT’。
        """
        params = {
            "sql": sql,
            "offset": offset,
            "limit": limit,
            "acceptPartial": acceptPartial,
            "project": project,
        }
        result = self._post("query/prepare", params=params)
        return result

    def api_save_query(self, sql, name, project, description=None):
        """
        保存查询

        参数：

        sql-必需 string sql语句的文本。
        name-必需 string Sql名称。
        project-必需 string Project执行查询。
        description-可选 string Sql描述。
        """
        params = {
            "sql": sql,
            "name": name,
            "project": project,
            "description": description,
        }
        result = self._post("saved_queries", params=params)
        return result

    def api_remove_saved_query(self, queryId):
        """
        删除已保存的查询
        参数：
        queryId - 必需 string 要删除的已保存查询的ID
        """
        result = self._del(
            "saved_queries/{queryId}".format(queryId=queryId))
        return result

    def api_get_saved_queries(self):
        """
        获取已保存的查询
        参数：无
        """
        result = self._get("saved_queries")
        return result

    def api_get_running_queries(self):
        """
        获取正在运行的查询
        参数：无
        """
        result = self._get("query/runningQueries")
        return result

    def api_stop_query(self, queryId):
        """
        停止正在运行的查询
        参数：
        queryId - 必需 string 要停止的查询ID。您可以通过获取运行查询来获取它。
        """
        result = self._get("query/{queryId}/stop".format(queryId=queryId))
        return result

    def api_list_queryable_tables(self, project=None):
        """
        获取可用于查询的表
        参数：
        project - 必需 string 项目
        """
        result = self._get("tables_and_columns")
        return result

    """
    +++++++++++++++++++++++++++Model 数据模型及相关API+++++++++++++++++++++++++++++++++
    """

    def api_get_data_model(self, modeName):
        """
        获取数据模型
        参数：
        modelName - 必需 string 数据模型名称，默认情况下应与多维数据集名称相同。
        """
        result = self._get("model/{modeName}".format(modeName=modeName))
        return result

    def api_create_model(self, modelName, modelDescData, projectName):
        """
        创建数据模型
        参数：
        modelName - 必需 string 数据模型名称
        modelDescData - 必需 string 数据模型数据简介
        projectName - 必需 string 数据模型所属的项目名称
        """
        params = {
            "modelName": modelName,
            "modelDescData": modelDescData,
            "project": projectName
        }
        result = self._post("models", params=params)
        return result

    def api_update_model(self, modelName, modelDescData, projectName):
        """
        更新数据模型
        参数：
        modelName - 必需 string 数据模型名称
        modelDescData - 必需 string 数据模型数据简介
        projectName - 必需 string 数据模型所属的项目名称
        """
        params = {
            "modelName": modelName,
            "modelDescData": modelDescData,
            "projectName": projectName
        }
        result = self._put("models", params=params)
        return result

    def api_get_model_desc_data(self, modelName=None, projectName=None, limit=None, offset=None):
        """
        获取模型描述数据
        modelName - 可选 string model名称。
        projectName - 可选 string 项目名称。
        limit - 可选 int 每页模型数量
        offset - 可选 int 分页使用的偏移量
        """
        params = {
            "modelName": modelName,
            "projectName": projectName,
            "limit": limit,
            "offset": offset,
        }
        result = self._get("models", params=params)
        return result

    def api_delete_model(self, modelName):
        """
        删除数据模型
        参数：
        modelName - 必需 string 数据模型名称
        """
        result = self._del(
            "models/{modelName}".format(modelName=modelName))
        return result

    def api_clone_model(self, modelName):
        """
        克隆数据模型
        参数：
        modelName - 必需 string 数据模型名称
        """
        result = self._put(
            "models/{modelName}/clone".format(modelName=modelName))
        return result

    """
    +++++++++++++++++++++++++++Cube多维数据集相关API+++++++++++++++++++++++++++++++++
    """

    def api_create_cube(self, cubeName, cubeDescData, projectName):
        """
        cubeName - 必需 string 多维数据的创建名称
        cubeDescData - 必需 string 多维数据集的数据简介
        projectName - 必需 string 多维数据集所属的项目名称
        """
        params = {
            "cubeName": cubeName,
            "cubeDescData": cubeDescData,
            "projectName": projectName
        }

        result = self._post("cubes", params=params)
        return result

    def api_update_cube(self, cubeName, cubeDescData, projectName):
        """
        cubeDescData - 必需 string 多维数据集的数据简介
        cubeName - 必需 string 多维数据的创建名称
        projectName - 必需 string 多维数据集所属的项目名称
        """
        params = {
            "cubeName": cubeName,
            "cubeDescData": cubeDescData,
            "projectName": projectName
        }

        result = self._put("cubes", params=params)
        return result

    def api_list_cubes(self, offset=0, limit=None, cubeName=None, projectName=None):
        """
        列出cube
        参数：
        offset - 必需 int 分页使用的偏移量
        limit - 必需 int 多维数据集。
        cubeName - 可选 string 多维数据集名称的关键字。查找名称包含此关键字的多维数据集。
        projectName - 可选 string 项目名称。

        """
        params = {
            "offset": offset,
            "limit": limit,
            "cubeName": cubeName,
            "projectName": projectName
        }
        result = self._get("cubes", params=params)
        return result

    def api_get_cube(self, cubeName):
        """
        获取某个cube
        参数：
        cubeName - 必需 string 要查找的多维数据集名称。
        """
        result = self._get("cubes/{cubeName}".format(cubeName=cubeName))
        return result

    def api_get_cube_descriptor(self, cubeName):
        """
        获取指定多维数据集实例的描述符。
        参数：
        cubeName - 必需 string 多维数据集名称。
        """
        result = self._get(
            "cube_desc/{cubeName}".format(cubeName=cubeName))
        return result

    def api_build_cube(self, cubeName, buildType, startTime=None, endTime=None):
        """
        构建立方体
        参数：
        cubeName - 必需 string 多维数据集名称。
        startTime - 可选 long 启动时间戳记，例如2014-1-1的1388563200000
        endTime- 可选 long 结束时间戳
        buildType-必需 的字符串支持的构建类型：“ BUILD”，“ MERGE”，“ REFRESH”
        """
        params = {
            "startTime": startTime,
            "endTime": endTime,
            "buildType": buildType,
        }
        result = self._put(
            "cube_desc/{cubeName}".format(cubeName=cubeName), params=params)
        return result

    def api_enable_cube(self, cubeName):
        """
        启用多维数据集
        参数：
        cubeName - 必需 string 多维数据集名称。
        """
        result = self._put(
            "cubes/{cubeName}/enable".format(cubeName=cubeName))
        return result

    def api_disable_cube(self, cubeName):
        """
        停用多维数据集
        参数：
        cubeName - 必需 string 多维数据集名称。
        """
        result = self._put(
            "cubes/{cubeName}/disable".format(cubeName=cubeName))
        return result

    def api_purge_cube(self, cubeName):
        """
        清除多维数据集
        参数：
        cubeName - 必需 string 多维数据集名称。
        """
        result = self._put(
            "cubes/{cubeName}/purge".format(cubeName=cubeName))
        return result

    def api_delete_segment(self, cubeName, segmentName):
        """
        删除分片
        参数：
        cubeName - 必需 string 多维数据集名称.
        segmentName - 必需 string 片段名称
        """
        result = self._del(
            "cubes/{cubeName}/segs/{segmentName}".format(cubeName=cubeName, segmentName=segmentName))
        return result

    def api_auto_merge_segment(self, cubeName):
        """
        自动合并片段
        参数：
        cubeName - 必需 string 多维数据集名称.
        """
        result = self._put(
            "cubes/{cubeName}/automerge".format(cubeName=cubeName))
        return result

    def api_get_sql_of_cube(self, cubeName):
        """
        获取多维数据集的SQL
        参数：
        cubeName - 必需 string 多维数据集名称.
        """
        result = self._get(
            "cubes/{cubeName}/sql".format(cubeName=cubeName))
        return result

    def api_get_sql_of_a_cube_segment(self, cubeName, segmentName):
        """
        获取多维数据集分段的SQL
        参数：
        cubeName - 必需 string 多维数据集名称.
        segmentName - 必需 string 分片名称
        """
        result = self._get(
            "cubes/{cubeName}/segs/{segmentName}/sql".format(cubeName=cubeName, segmentName=segmentName))
        return result

    def api_force_rebuild_lookup_table_snapshot(self, cubeName):
        """
        强制重建查找表快照
        参数：
        cubeName - 必需 string 多维数据集名称.
        """
        result = self._put(
            "cubes/{cubeName}/refresh_lookup".format(cubeName=cubeName))
        return result

    def api_clone_cube(self, cubeName):
        """
        克隆多维数据集
        参数：
        cubeName - 必需 string 多维数据集名称.
        """
        result = self._put(
            "cubes/{cubeName}/clone".format(cubeName=cubeName))
        return result

    def api_delete_cube(self, cubeName):
        """
        删除多维数据集
        参数：
        cubeName - 必需 string 多维数据集名称.
        """
        result = self._del("cubes/{cubeName}".format(cubeName=cubeName))
        return result

    def api_migrate_cube(self, cubeName, projectName):
        """
        迁移多维数据集
        参数：
        cubeName - 必需 string 多维数据集名称.
        projectName - 必需 string 项目名称。
        """
        result = self._post(
            "cubes/{cubeName}/{projectName}/migrate".format(cubeName=cubeName, projectName=projectName))
        return result

    def api_get_hbase_info(self, cubeName):
        """
        获取多维数据集的hbase信息
        参数：
        cubeName - 必需 string 多维数据集名称.
        """
        result = self._del(
            "cubes/{cubeName}/hbase".format(cubeName=cubeName))
        return result

    def api_get_current_cuboid(self, cubeName):
        """
        获取当前的Cuboid。Cuboid在kylin中指定在某一种维度组合下所有计算的数据
        参数：
        cubeName - 必需 string 多维数据集名称.
        """
        result = self._del(
            "cubes/{cubeName}/cuboids/current".format(cubeName=cubeName))
        return result

    def api_initiate_cube_start_position(self, cubeName):
        """
        启动多维数据集开始位置
        将流式多维数据集的开始位置设置为当前的最新偏移量；这样可以避免从Kafka主题的最早列表位置建立（如果您设置了较长的保留时间）；
        参数：
        cubeName - 必需 string 多维数据集名称.
        """
        result = self._put(
            "cubes/{cubeName}/init_start_offsets".format(cubeName=cubeName))
        return result

    def api_build_stream_cube(self, cubeName, sourceOffsetStart, sourceOffsetEnd, buildType):
        """
        构建流多维数据集
        该API专用于Stream cube的构建；
        参数：
        cubeName - 必需 string 多维数据集名称.
        sourceOffsetStart - 必需 long 起始偏移量，0表示从上一个位置开始；
        sourceOffsetEnd - 必需 long 结束偏移量9223372036854775807表示当前流数据的结束位置
        buildType - 必需 string 构建类型， “BUILD”, “MERGE” or “REFRESH”
        """
        params = {
            "sourceOffsetStart": sourceOffsetStart,
            "sourceOffsetEnd": sourceOffsetEnd,
            "buildType": buildType,
        }
        result = self._put(
            "cubes/{cubeName}/build2".format(cubeName=cubeName), params=params)
        return result

    def api_chaeck_segment_holes(self, cubeName):
        """
        检查分段缺口
        参数：
        cubeName - 必需 string 多维数据集名称.
        """
        result = self._get(
            "cubes/{cubeName}/holes".format(cubeName=cubeName))
        return result

    def api_full_segment_holes(self, cubeName):
        """
        填充分段缺口
        参数：
        cubeName - 必需 string 多维数据集名称.
        """
        result = self._put(
            "cubes/{cubeName}/holes".format(cubeName=cubeName))
        return result

    """
    +++++++++++++++++++++++++++任务相关API+++++++++++++++++++++++++++++++++
    """

    def api_get_job_list(self, projectName, offset, limit, timeFilter, cubeName=None, status=None):
        """
        获取工作清单
        参数：
        cubeName - 可选 string 多维数据集名称。
        projectName - 必需 string 项目名称。
        status - 可选 int 作业状态，例如（新功能：0，待处理：1，正在运行：2，已停止：32，已完成：4，错误：8，已拒绝：16）
        offset - 必需 int 分页使用的偏移量。
        limit - 必需 int 每页作业数量。
        timeFilter - 必需  int 时间筛选，例如（最近一天：0，最近一周：1，最近一个月：2，最近一年：3，全部：4）
        """
        params = {
            "cubeName": cubeName,
            "projectName": projectName,
            "status": status,
            "offset": offset,
            "limit": limit,
            "timeFilter": timeFilter,
        }
        result = self._get("jobs", params=params)
        return result

    def api_get_job_status_overview(self, projectName, offset, limit, timeFilter, cubeName=None, status=None):
        """
        获取作业状态概述
        参数：
        cubeName - 可选 string 多维数据集名称。
        projectName - 必需 string 项目名称。
        status - 可选 int 作业状态，例如（新功能：0，待处理：1，正在运行：2，已停止：32，已完成：4，错误：8，已拒绝：16）
        offset - 必需 int 分页使用的偏移量。
        limit - 必需 int 每页作业数量。
        timeFilter - 必需  int 时间筛选，例如（最近一天：0，最近一周：1，最近一个月：2，最近一年：3，全部：4）
        """
        params = {
            "cubeName": cubeName,
            "projectName": projectName,
            "status": status,
            "offset": offset,
            "limit": limit,
            "timeFilter": timeFilter,
        }
        result = self._get("jobs/overview", params=params)
        return result

    def api_resume_job(self, jobId):
        """
        恢复任务
        参数：
        jobId - 必须 string 任务ID
        """
        result = self._put("jobs/{jobId}/resume".format(jobId=jobId))
        return result

    def api_discard_job(self, jobId):
        """
        放弃任务
        参数：
        jobId - 必须 string 任务ID
        """
        result = self._put("jobs/{jobId}/discard".format(jobId=jobId))
        return result

    def api_drop_job(self, jobId):
        """
        删除任务
        参数：
        jobId - 必须 string 任务ID
        """
        result = self._del("jobs/{jobId}/drop".format(jobId=jobId))
        return result

    def api_get_job_status(self, jobId):
        """
        获取任务状态
        参数：
        jobId - 必须 string 任务ID
        """
        result = self._get("jobs/{jobId}".format(jobId=jobId))
        return result

    def api_get_job_step_output(self, jobId, stepId):
        """
        获取任务步骤的输出
        参数：
        jobId - 必需 string 作业ID。
        stepId - 必需 string 步骤ID；步骤ID由jobId和步骤序列ID组成。
        例如，jobId为“ fb479e54-837f-49a2-b457-651fc50be110”，其第3步id为“ fb479e54-837f-49a2-b457-651fc50be110-3”，

        """
        result = self._get(
            "jobs/{jobId}/steps/{stepId}/output".format(jobId=jobId, stepId=stepId))
        return result

    def api_resubmit_realtime_build_job(self, jobId):
        """
        重新提交实时构建作业
        参数：
        jobId - 必须 string 任务ID
        """
        result = self._put("jobs/{jobId}/resubmit".format(jobId=jobId))
        return result

    def api_rollback_job(self, jobId, stepId):
        """
        回滚作业
        参数：
        jobId - 必需 string 您要回滚的工作ID.
        stepId - 必需 string 步骤ID；指定回滚步骤ID，例如（Create Intermediate Flat Hive：1）

        """
        result = self._put(
            "jobs/{jobId}/steps/{stepId}/rollbackt".format(jobId=jobId, stepId=stepId))
        return result

    """
    +++++++++++++++++++++++++++hive相关API+++++++++++++++++++++++++++++++++
    """

    def api_get_hive_table(self, tableName):
        """
        根据表名获取hive表

        参数：
        tableName - 必需 string 查找的表名称。
        """
        result = self._get(
            "tables/{tableName}".format(tableName=tableName))
        return result

    def api_get_hive_table_ext(self, tableName):
        """
        根据表名获取hive表(扩展信息)

        参数：
        tableName - 必需 string 查找的表名称。
        """
        result = self._get(
            "tables/{tableName}/exd-map".format(tableName=tableName))
        return result

    def api_get_hive_tables(self, project, ext=False):
        """
        获取hive表

        参数：
        project -必需 string 将列出项目中的所有表。
        ext - 可选 boolean 设置为true可获得表的扩展信息。
        """
        params = {
            "project": project,
            "ext": ext
        }
        result = self._get("tables", params=params)
        return result

    def api_load_hive_tables(self, tables, project, calculate=False):
        """
        加载hive表
        参数：
        table -  必需 string 您要从配置单元中加载的表名称，以逗号分隔。
        project - 必需 string 表将加载到的项目。

        """
        params = {
            "calculate": calculate,
        }
        result = self._post(
            "tables/{tables}/{project}".format(tables=tables, project=project), params=params)
        return result

    def api_unload_hive_tables(self, tables, project):
        """
        卸载hive表
        参数：
        table -  必需 string 要卸载的表名，以逗号分隔。
        project - 必需 string 表所属的项目。

        """
        result = self._del(
            "tables/{tables}/{project}".format(tables=tables, project=project))
        return result

    def api_show_database_in_hive(self):
        """
        在配置单元中显示数据库
        参数：无
        """
        result = self._get("tables/hive")
        return result

    def api_show_table_in_hive_database(self, databaseName):
        """
        显示配置单元数据库中的表
        参数：
        databaseName - 必需 string hive数据库名称
        """
        result = self._get(
            "tables/hive/{databaseName}".format(databaseName=databaseName))
        return result

    def api_get_user_can_query_query_the_table(self, project, utype, table):
        """
        获取用户可以查询表
        参数：
        project - 必需 string 表所属的projectName
        utype - 必需 string 用户或组
        table - 必需 string 表名称
        """
        result = self._get(
            "acl/table/{project}/{type}/{table}".format(project=project, utype=utype, table=table))
        return result

    def api_get_user_cannot_query_query_the_table(self, project, utype, table):
        """
        获取用户不可以查询表
        参数：
        project - 必需 string 表所属的projectName
        utype - 必需 string 用户或组
        table - 必需 string 表名称
        """
        result = self._get(
            "acl/table/{project}/{type}/black/{table}".format(project=project, utype=utype, table=table))
        return result

    def api_put_user_2_table_blacklist(self, project, utype, table, name):
        """
        将用户放入表黑名单
        参数：
        project - 必需 string 表所属的projectName
        utype - 必需 string 用户或组
        table - 必需 string 表名称
        name - 必需 string 要放入表黑名单的用户名或组名
        """
        result = self._del("table/{project}/{type}/{table}/{name}".format(
            project=project, utype=utype, table=table, name=name))
        return result

    def api_delete_user_from_table_blacklist(self, project, utype, table, name):
        """
        将用户从表黑名单删除
        参数：
        project - 必需 string 表所属的projectName
        utype - 必需 string 用户或组
        table - 必需 string 表名称
        name - 必需 string 要放入表黑名单的用户名或组名
        """
        result = self._post("table/{project}/{type}/{table}/{name}".format(
            project=project, utype=utype, table=table, name=name))
        return result

    """
    +++++++++++++++++++++++++++cache相关API+++++++++++++++++++++++++++++++++
    """

    def api_wipe_cache(self, name, ctype, action):
        """
        清除缓存
        参数：
        ctype - 必需 string ‘METADATA’ or ‘CUBE’
        name - 必需 string 缓存键，例如多维数据集名称。
        action - 必需 string ‘create’, ‘update’ or ‘drop’
        """
        result = self._put(
            "cache/{ctype}/{name}/{action}".format(ctype=ctype, name=name, action=action))
        return result

    def api_announce_wipe_cache(self, name, ctype, action):
        """
        宣布清除缓存
        参数：
        ctype - 必需 string ‘METADATA’ or ‘CUBE’
        name - 必需 string 缓存键，例如多维数据集名称。
        action - 必需 string ‘create’, ‘update’ or ‘drop’
        """
        result = self._put(
            "cache/announce/{ctype}/{name}/{action}".format(ctype=ctype, name=name, action=action))
        return result

    def api_hot_load_kylin_config(self):
        """
        热载Kylin配置
        参数：无
        """
        result = self._post("cache/announce/config")
        return result

    """
    +++++++++++++++++++++++++++streaming 相关API+++++++++++++++++++++++++++++++++
    """

    def api_get_streaming_config(self):
        """
        获取流媒体配置
        参数：无
        """
        result = self._get("streaming/getConfig")
        return result

    def api_get_kafka_config(self):
        """
        获取流媒体配置
        参数：无
        """
        result = self._get("streaming/getKfkConfig")
        return result

    def api_create_streaming_schema(self, project, tableData, StreamingConfig, kafkaConfig):
        """
        创建流模式
        参数：
        project - 必需 string 您要创建流模式的项目。
        tableData - 必需 string 流表desc。
        StreamingConfig - 必需 string Streaming配置。
        kafkaConfig - 必需 string Kafka配置。
        """
        params = {
            "project": project,
            "tableData": tableData,
            "StreamingConfig": StreamingConfig,
            "kafkaConfig": kafkaConfig,
        }
        result = self._post("streaming", params=params)
        return result

    def api_update_streaming_schema(self, project, tableData, StreamingConfig, kafkaConfig):
        """
        更新流模式
        参数：
        project - 必需 string 您要更新流模式的项目。
        tableData - 必需 string 流表desc。
        StreamingConfig - 必需 string Streaming配置。
        kafkaConfig - 必需 string Kafka配置。
        """
        params = {
            "project": project,
            "tableData": tableData,
            "StreamingConfig": StreamingConfig,
            "kafkaConfig": kafkaConfig,
        }
        result = self._post("streaming", params=params)
        return result

    """
    +++++++++++++++++++++++++++metrics相关API+++++++++++++++++++++++++++++++++
    """

    def api_get_all_metrics(self):
        """
        获取所有指标
        参数：无

        """
        result = self._get("jmetrics")
        return result

    def api_get_apecific_type_of_metrics(self, mtype):
        """
        获取特定类型的指标
        参数：
        mtype - 必需 string 所需的度量标准的特定类型
        """
        result = self._get("jmetrics/{mtype}".format(mtype=mtype))
        return result

