#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD
import os

from flask import Blueprint, jsonify, request, current_app
from dmp.utils import resp_hanlder, uuid_str
from dmp.models import FromDownload

file = Blueprint("file", __name__)


@file.route("/upload/", methods=["POST"], defaults={"desc": {"interface_name": "文件上传","is_permission": False,"permission_belong": None}})
def upload(desc):
    if request.method == 'POST':
        try:
            # current_app.logger.info(current_app.config)
            upload_file = request.files['file']
            # 获取文件唯一标识符
            task = request.form.get('task_id')
            # 获取该分片在所有分片中的序号
            chunk = request.form.get('chunk', 0)
            # 构成该分片唯一标识符
            filename = '%s%s' % (task, chunk)
            # 保存分片到本地
            upload_file.save(os.path.join(current_app.config.get("UPLOADED_PATH"), filename))
            return resp_hanlder()
        except Exception as err:
            current_app.logger.error(err)
            return resp_hanlder(err=err)


@file.route("/success/", methods=["GET"], defaults={"desc": {"interface_name": "文件上传完成","is_permission": False,"permission_belong": None}})
def success(desc):
    target_filename = request.json.get('filename')
    task = request.args.get('task_id')
    chunk = 0
    upload_path = current_app.config.get("UPLOADED_PATH")
    current_app.logger.info("%s%s%s" % (target_filename, task, upload_path))
    finally_filename = uuid_str() + target_filename
    with open(os.path.join(upload_path, finally_filename), 'wb') as target_file:
        while True:
            try:
                filename = os.path.join(upload_path, '%s%d' % (task, chunk))
                current_app.logger.info(filename)
                # 按序打开每个分片
                source_file = open(filename, 'rb')
                # 读取分片内容写入新文件
                target_file.write(source_file.read())
                source_file.close()
            except IOError:
                break
            chunk += 1
            # 删除该分片，节约空间
            os.remove(filename)
    current_app.logger.info(finally_filename)
    return resp_hanlder(result={"filename": finally_filename})


class FormDownload(object):
    pass


@file.route("/dlcomplete/", methods=["GET"], defaults={"desc": {"interface_name": "文件下载完成","is_permission": False,"permission_belong": None}})
def dlcomplete(desc):
    if request.method == "GET":
        try:
            form_id = request.json.get("form_id")
            form_ = FromDownload.get(form_id)
            rm_filepath = form_.filepath
            os.remove(rm_filepath)
            return resp_hanlder(result="OK")
        except Exception as err:
            return resp_hanlder(result="OK")
