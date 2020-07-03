#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : SHTD 


def hct():
    from dmp.models import DataTable
    h = DataTable.get(1)
    h.data_count()