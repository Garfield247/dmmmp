#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD
import os

from flask import Blueprint, jsonify, request, current_app
from dmp.utils import resp_hanlder,uuid_str

file = Blueprint("file", __name__)


@file.route("/upload/", methods=["POST"], defaults={"desc": "文件上传"})
def upload(desc):
    if request.method == 'POST':
        try:
            current_app.logger.info(current_app.config)
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
            return resp_hanlder()


@file.route("/success/", methods=["GET"], defaults={"desc": "文件上传完成"})
def success(desc):
    target_filename = request.query.get('filename')
    task = request.args.get('task_id')
    chunk = 0
    upload_path = current_app.config.get("UPLOADED_PATH")
    current_app.logger.info("%s%s%s"%(target_filename,task,upload_path))
    finally_filename = uuid_str()+target_filename
    with open(os.path.join(upload_path, finally_filename), 'wb') as target_file:
        while True:
            try:
                filename = os.path.join(upload_path, '%s%d'%(task, chunk))
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
    return resp_hanlder(result={"filename": target_filename})


@file.route("/dlcomplete/", methods=["GET"], defaults={"desc": "文件下载完成"})
def dlcomplete(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)
