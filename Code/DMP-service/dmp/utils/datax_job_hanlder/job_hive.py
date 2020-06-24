#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/25
# @Author  : SHTD 


def hive_reader(host,port,path,fileType,column,fieldDelimiter=",",encoding="UTF-8",):
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
        "name": "hdfsreader",
        "parameter": {
            "path": path,
            "defaultFS": "hdfs://%s:%d"%(host,port),
            "column": column ,
            "fileType": fileType,
            "encoding": encoding or "UTF-8",
            "fieldDelimiter": fieldDelimiter,
            "csvReaderConfig": {
                "safetySwitch": False,
                "skipEmptyRecords": False,
                "useTextQualifier": False
            }
        }
    }
    return hive_reader_json



def hive_writer(host,port,path,filename,column,fieldDelimiter=","):
    hive_writer_json = {
        "name": "hdfswriter",
        "parameter": {
            "defaultFS": "hdfs://%s:%d"%(host,port),
            "fileType": "text",
            "path": path,
            "fileName": filename,
            "column": column,
            "writeMode": "append",
            "fieldDelimiter":fieldDelimiter,
        }
    }
    return hive_writer_json
