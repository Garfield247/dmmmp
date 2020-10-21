#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/10/20
# @Author  : SHTD



from flask import current_app
from dmp.models import Database, DataTable, KylinTable
from dmp.utils.kylintool import kt, project
from dmp.utils import uuid_str



def modelDescData_hanlder(project,tableName,modelName,description):

    kt = KylinTool(
            host = current_app.config.get("KYLIN_HOST"),
            port = current_app.config.get("KYLIN_PORT"),
            user = current_app.config.get("KYLIN_USER"),
            passwd = current_app.config.get("KYLIN_PASSWD")
            )
    project = current_app.config.get("KYLIN_PROJECT")
    modelDescData_tmp = {
        "name": "",
        "description": "",
        "fact_table": "",
        "lookups": [],
        "filter_condition": "",
        "dimensions": [
        {
          "table": "",
          "columns": []
        }
        ],
        "metrics": [],
        "partition_desc": {
        "partition_type": "APPEND",
        "partition_date_format": "yyyy-MM-dd"
        },
        "last_modified": 0
        }
    modelDescData_tmp["name"] = modelName
    modelDescData_tmp["fact_table"] = tableName.upper()
    modelDescData_tmp["dimensions"] = [
        {
            "table":tableName.split(".")[1].upper(),
            "columns":[col.get("name") for col in kt.api_get_hive_table(project=project,tableName=tableName).get("columns")]
        }
    ]
    print(modelDescData_tmp)
    return modelDescData_tmp

def cubeDescDataHanlder(cubeName,modelsName,tableName,description,project):
    cubeDescDataTmp = {
      "name": cubeName,
      "model_name": modelsName,
      "description": description,
      "dimensions": [
          {"name": col.get("name"),
           "table": tableName.split(".")[1],
           "derived": None,
           "column": col.get("name")
          } for col in kt.api_get_hive_table(project=project,tableName=tableName).get("columns")
      ],
      "measures": [
        {
          "name": "_COUNT_",
          "function": {
            "expression": "COUNT",
            "returntype": "bigint",
            "parameter": {
              "type": "constant",
              "value": "1",
              "next_parameter": None
            },
            "configuration": {}
          }
        }
      ],
      "dictionaries": [],
      "rowkey": {
        "rowkey_columns": [
            {"column": "%s.%s"%(tableName.split(".")[1],col.get("name")),
             "encoding": "dict",
             "isShardBy": "false",
             "encoding_version": 1
            }   for col in kt.api_get_hive_table(project=project,tableName=tableName).get("columns")
        ]
      },
      "aggregation_groups": [
        {
          "includes": [],
          "select_rule": {
            "hierarchy_dims": [],
            "mandatory_dims": [],
            "joint_dims": []
          }
        }
      ],
      "mandatory_dimension_set_list": [],
      "partition_date_start": 0,
      "notify_list": [],
      "hbase_mapping": {
        "column_family": [
          {
            "name": "F1",
            "columns": [
              {
                "qualifier": "M",
                "measure_refs": [
                  "_COUNT_"
                ]
              }
            ]
          }
        ]
      },
      "volatile_range": "0",
      "retention_range": "0",
      "status_need_notify": [
        "ERROR",
        "DISCARDED",
        "SUCCEED"
      ],
      "auto_merge_time_ranges": [
        604800000,
        2419200000
      ],
      "engine_type": "2",
      "storage_type": "2",
      "override_kylin_properties": {}
    }
    return cubeDescDataTmp

def hive2kylin(hive_table_id):
    if DataTable.exist_item_by_id(hive_table_id):
        hive_table = DataTable.get(hive_table_id)
        if hive_table.dmp_database_id==1:
            table_name = "%s.%s"%(hive_table.dmp_database_name,hive_table.db_table_name)
            if KylinTable.exist_item_by_db_table_name(table_name):
                kt_item = KylinTable.query.filter_by(db_table_name=table_name).first()
                hive_table.kylin_info_id = kt_item.id
                hive_table.save()
            else:
                # load hive data
                load_hive_table_res = kt.api_load_hive_tables(
                    tables= load_table_name,
                    project=project
                    )
                if load_hive_table_res.get("result.loaded") == table_name.upper():
                    # 创建model
                    modelName = "model_%s_%s"%(table_name, uuid_str())
                    modelDescData = modelDescData_hanlder(
                            project=project,
                            tableName=table_name,
                            modelName=modelName
                            description=""
                            )
                    kt.api_create_model(
                            modelName = modelName,
                            projectName = project
                            )
                    # 创建cube
                    cubeName = "cube_%s_%s"%(table_name, uuid_str())
                    cubeDescData = cubeDescDataHanlder(
                            cubeName=cubeName,
                            description="",
                            tableName= table_name,
                            project= project,
                            modelsName=modelName
                            )
                    kt.api_create_cube(
                            cubeName=cubeName,
                            cubeDescData=cubeDescData,
                            projectName=project
                            )
                    # build cube
                    kt.api_build_cube(
                        cubeName=cubeName,
                        buildType="BUILD"
                        )




        else:
            raise Exception("数据库类型不符")
    else:
        return resp_hanlder(code=999, msg="数据表不存在或已被删除")





