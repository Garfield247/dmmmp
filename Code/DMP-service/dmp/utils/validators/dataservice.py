#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName  :dataservice.py
# @Time      :2020/9/28 18:14

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length


class DataServiceForm(FlaskForm):
    data_service_name = StringField("data_service_name",
                                    validators=[DataRequired(message="API名称不能为空"),
                                                Length(max=50, message="API名称长度不能超过50!")])
    api_path = StringField("api_path",
                           validators=[DataRequired(message="API路径不能为空"), Length(max=255, message="API路径长度不能超过255!")])
    request_method = SelectField("request_method", choices={1})
    description = StringField("description", validators=[Length(max=400, message="API描述长度不能超过400")])


class DataServiceParameterForm(FlaskForm):
    parameter_name = StringField("parameter_name",
                                 validators=[DataRequired(message="参数名不能为空"),
                                             Length(max=100, message="参数名长度不能超过100!")])
    type = StringField("type", validators=[DataRequired(), Length(max=50, message="字段类型长度不能超过50!")])
    required_parameter = SelectField("required_parameter", choices={0, 1})
    description = StringField("description", validators=[Length(max=400, message="简介长度不能超过400")])
