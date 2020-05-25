#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/25
# @Author  : SHTD 


def hive_reader(host,port,path,column,fileType,fieldDelimiter,encoding,haveKerberos,kerberosKeytabFilePath,kerberosPrincipal):
    """

    :param host:
    :param port:
    :param path:
    :param column:
    :param fileType:
    :param fieldDelimiter:
    :param encoding:
    :param haveKerberos:
    :param kerberosKeytabFilePath:
    :param kerberosPrincipal:
    :return:
    """
    hive_reader_json = {
        "name": "hdfs_reader",
        "parameter": {
            "path": path,
            "defaultFS": "hdfs://%s:%d"%(host,port),
            "column": column if column else ["*"],
            "fileType": fileType,
            "encoding": encoding or "UTF-8",
            "fieldDelimiter": fieldDelimiter or ",",
            "csvReaderConfig": {
                "safetySwitch": False,
                "skipEmptyRecords": False,
                "useTextQualifier": False
            }
        }
    }
    return hive_reader_json



def hive_writer(host,port):
    hive_writer_json = {
        "name": "hdfs_writer",
        "parameter": {
            "defaultFS": "hdfs://%s:%d"%(host,port),
            "fileType": "orc",
            "path": "/user/hive/warehouse/writerorc.db/orcfull",
            "fileName": "xxxx",
            "column": [],
            "writeMode": "append",
            "fieldDelimiter": "\t",
            "compress": "NONE"
        }
    }

