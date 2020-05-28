#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/28
# @Author  : SHTD 


def textfile_reader(filepath,column,encoding="UTF-8",fieldDelimiter=","):
    textfile_reader_json = {
                    "name": "txtfilereader",
                    "parameter": {
                        "path": [filepath],
                        "encoding": encoding,
                        "column": column,
                        "fieldDelimiter": fieldDelimiter,
                    }}
    return textfile_reader_json


def textfile_writer(filepath,filename,header,encoding="UTF-8"):
    textfile_writer_json = {
        "name": "txtfilewriter",
        "parameter": {
            "path": filepath,
            "fileName": filename,
            "writeMode": "truncate",
            "encoding" : encoding,
            "header":header
        }
    }
    return textfile_writer_json