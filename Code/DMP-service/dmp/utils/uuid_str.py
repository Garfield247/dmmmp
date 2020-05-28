#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

import uuid


def uuid_str():
    uuid_obj = uuid.uuid1()
    uuid_obj_str = str(uuid_obj)
    uuid_list = uuid_obj_str.split('-')
    uuid_img_name = uuid_list[0] + uuid_list[3]
    return uuid_img_name
