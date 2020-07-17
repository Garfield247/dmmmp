#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/7/14
# @Author  : SHTD 

import datetime
from dmp.extensions import db
from dmp.models import DMPModel


class Forms(db.Model, DMPModel):
    """表单总表"""
    __tablename__ = 'dmp_form'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    submit_dmp_user_id = db.Column(db.Integer, nullable=False, comment='提交人')
    submit_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='提交时间')
    description = db.Column(db.Text, comment='说明')

    approve_dmp_user_id = db.Column(db.Integer, comment='审批人')
    approve_on = db.Column(db.DateTime, comment='审批时间')
    approve_result = db.Column(db.Integer, default=0, comment='审批结果,默认:0,通过:1,不通过:2')
    answer = db.Column(db.String(32), comment='审批答复')

    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')

    form_type = db.Column(db.Integer, default=1, comment='表单类型')
    form_info_id = db.Column(db.Integer,nullable=False, comment='表单详情ID ')

    finish = db.Column(db.Boolean,default=False, comment='是否完成')
    result = db.Column(db.Text, comment='结果')

    __mapper_args__ = {
        "order_by": submit_on.desc()
    }

    @property
    def submit_dmp_username(self):
        from dmp.models import Users
        u = Users.get(self.submit_dmp_user_id)
        s_u_name = u.dmp_username if u else "-"
        return s_u_name

    @property
    def approve_dmp_username(self):
        from dmp.models import Users
        u = Users.get(self.approve_dmp_user_id)
        a_u_name = u.dmp_username if u else "-"
        return a_u_name

    @property
    def info_form(self):
        from dmp.models import FormAddDataTable,FormUpload,FormMigrate,FormDownload
        form_type_map = {
            1:FormAddDataTable,
            2:FormUpload,
            3:FormMigrate,
            4:FormDownload
        }
        form_info = form_type_map.get(self.form_type).get(self.form_info_id)
        return form_info

    @property
    def _json_tmp(self):
        _d = {
            "submit_dmp_username":self.submit_dmp_username,
            "approve_dmp_username": self.approve_dmp_username,
        }

        info_d = self.info_form.__json__()
        _d.update(info_d)
        return _d