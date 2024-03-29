#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD
import os

import pandas as pd
from flask import Blueprint,  request, current_app
from dmp.utils import resp_hanlder, uuid_str
from dmp.models import Forms

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
    target_filename = request.args.get('filename')
    task = request.args.get('task_id')
    filetype = int(request.args.get("filetype")) or 1

    current_app.logger.info(request.args)
    chunk = 0
    upload_path = current_app.config.get("UPLOADED_PATH")
    current_app.logger.info("%s%s%s" % (target_filename, task, upload_path))
    tmp_filename = uuid_str() + "_TMP_" +target_filename
    finally_filename = uuid_str() + target_filename
    with open(os.path.join(upload_path, tmp_filename), 'wb') as target_file:
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
    if filetype == 1:
        os.rename(os.path.join(upload_path, tmp_filename),os.path.join(upload_path, finally_filename))
    elif filetype == 2:
        data = pd.read_json(os.path.join(upload_path, tmp_filename))
        data.to_csv(os.path.join(upload_path, finally_filename))
    elif filetype == 3:
        data = pd.read_excel(os.path.join(upload_path, tmp_filename))
        data.to_csv(os.path.join(upload_path, finally_filename))
    current_app.logger.info(finally_filename)
    return resp_hanlder(result={"filename": finally_filename})





@file.route("/dlcomplete/", methods=["GET"], defaults={"desc": {"interface_name": "文件下载完成","is_permission": False,"permission_belong": None}})
def dlcomplete(desc):
    if request.method == "GET":
        try:
            form_id = request.json.get("form_id")
            form_ = Forms.get(form_id)
            rm_filepath = form_.info_form.filepath
            if os.path.exists(rm_filepath):
                os.remove(rm_filepath)
            dlform = form_.info_form
            dlform.ftp_url = None
            dlform.filepath = None
            dlform.put()
            return resp_hanlder(result="OK")


        except Exception as err:
            return resp_hanlder(result="OK")
