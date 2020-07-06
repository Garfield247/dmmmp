#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

import datetime
from dmp.extensions import db
from dmp.models import DMPModel


class FromMigrate(db.Model, DMPModel):
    """数据迁移表单表"""
    __tablename__ = 'dmp_from_migrate'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rule = db.Column(db.String(64), comment='数据库提取规则')
    new_table_name = db.Column(db.String(32), nullable=False, comment='新表名')
    description = db.Column(db.Text, comment='说明')
    submit_on = db.Column(db.DateTime, nullable=False,default=datetime.datetime.now, comment='提交时间')
    approve_on = db.Column(db.DateTime,onupdate=datetime.datetime.now, comment='审批时间')
    approve_result = db.Column(db.Integer, default=0, comment='审批结果,默认:0,通过:1,不通过:2')
    answer = db.Column(db.String(32), comment='审批答复')
    migrate = db.Column(db.Boolean, comment='迁移成功')
    migrate_result = db.Column(db.String(32), comment='迁移结果')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    submit_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), nullable=False, comment='提交人')
    origin_dmp_table_id = db.Column(db.Integer, db.ForeignKey('dmp_data_table.id'), nullable=False, comment='起点数据表')
    destination_dmp_database_id = db.Column(db.Integer, db.ForeignKey('dmp_database.id'), nullable=False,
                                            comment='目标数据库ID')
    approve_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), comment='审批人')
    form_type = db.Column(db.Integer, default=3, comment='表单类型')

    submit_users = db.relationship('Users', foreign_keys=submit_dmp_user_id, backref='submit_users_from_migrate')
    approve_users = db.relationship('Users', foreign_keys=approve_dmp_user_id, backref='approve_users_from_migrate')
    datatable = db.relationship('DataTable', backref='datatable_from_migrate')
    database = db.relationship('Database', backref='database_from_migrate')
