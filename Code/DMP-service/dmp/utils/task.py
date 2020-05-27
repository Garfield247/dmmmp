#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from dmp.extensions import celery

@celery.task
def add(x, y):
    return x + yce