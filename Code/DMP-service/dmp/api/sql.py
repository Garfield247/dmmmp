#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : SHTD

from flask import Blueprint
from dmp.utils.engine import auto_connect
from flask import Blueprint, request
from dmp.utils import resp_hanlder
from dmp.utils.engine import auto_connect
from dmp.utils.validators.dataservice import DataServiceForm, DataServiceParameterForm
from dmp.models import SavedQuery


sql = Blueprint("sql", __name__)


@sql.route("/queries", methods=["GET"],defaults={"desc": {"interface_name": "获取多个保存的SQL", "is_permission": True, "permission_belong": 0}})
def get_data_services(desc):

    """
    获取多个保存的SQL

    ---
    tags:
      - SQL
    parameters:
      - name: <++>
        in: <++>
        type: <++>
        required: <++>
        description: <++>
    responses:
      <++>:
        description: <++>
        schema:
          id: result
          properties:
            <++>:
              type: <++>
              description: <++>
              default: <++>
            <++>:
              type: <++>
              description: <++>
              items:
                type: <++>
              default: ["<++>", "<++>", "<++>"]
	"""

@sql.route("/queries/<int:query_id>", methods=["GET"],defaults={"desc": {"interface_name": "根据ID获取保存的SQL", "is_permission": True, "permission_belong": 0}})
def get_data_services(desc):

    """
    根据ID获取保存的SQL

    ---
    tags:
      - SQL
    parameters:
      - name: <++>
        in: <++>
        type: <++>
        required: <++>
        description: <++>
    responses:
      <++>:
        description: <++>
        schema:
          id: result
          properties:
            <++>:
              type: <++>
              description: <++>
              default: <++>
            <++>:
              type: <++>
              description: <++>
              items:
                type: <++>
              default: ["<++>", "<++>", "<++>"]
	"""

@sql.route("/queries", methods=["POST"],defaults={"desc": {"interface_name": "保存SQL", "is_permission": True, "permission_belong": 0}})
def get_data_services(desc):

    """
    保存SQL

    ---
    tags:
      - SQL
    parameters:
      - name: <++>
        in: <++>
        type: <++>
        required: <++>
        description: <++>
    responses:
      <++>:
        description: <++>
        schema:
          id: result
          properties:
            <++>:
              type: <++>
              description: <++>
              default: <++>
            <++>:
              type: <++>
              description: <++>
              items:
                type: <++>
              default: ["<++>", "<++>", "<++>"]
	"""

@sql.route("/queries/<int:query_id>", methods=["PUT"],defaults={"desc": {"interface_name": "获取多个保存的SQL", "is_permission": True, "permission_belong": 0}})
def get_data_services(desc):

    """
    获取多个保存的SQL

    ---
    tags:
      - SQL
    parameters:
      - name: <++>
        in: <++>
        type: <++>
        required: <++>
        description: <++>
    responses:
      <++>:
        description: <++>
        schema:
          id: result
          properties:
            <++>:
              type: <++>
              description: <++>
              default: <++>
            <++>:
              type: <++>
              description: <++>
              items:
                type: <++>
              default: ["<++>", "<++>", "<++>"]
	"""
@sql.route("/queries", methods=["GET"],defaults={"desc": {"interface_name": "获取多个保存的SQL", "is_permission": True, "permission_belong": 0}})
def get_data_services(desc):

    """
    获取多个保存的SQL

    ---
    tags:
      - SQL
    parameters:
      - name: <++>
        in: <++>
        type: <++>
        required: <++>
        description: <++>
    responses:
      <++>:
        description: <++>
        schema:
          id: result
          properties:
            <++>:
              type: <++>
              description: <++>
              default: <++>
            <++>:
              type: <++>
              description: <++>
              items:
                type: <++>
              default: ["<++>", "<++>", "<++>"]
	"""
