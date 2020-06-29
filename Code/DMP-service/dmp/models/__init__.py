#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from datetime import datetime, date

from sqlalchemy import inspect
from flask import json as _json, current_app

from dmp.extensions import db
from dmp.utils.wetime import default_date_format, default_datetime_format


class DMPModel(object):
    @classmethod
    def get(cls, primary_key):
        return cls.query.get(primary_key)

    @property
    def persistent(self):
        return inspect(self).persistent

    def put(self):
        if self.persistent:
            self._json_cache = self.__json__()
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    @classmethod
    def commit(cls):
        db.session.commit()

    @classmethod
    def rollback(cls):
        db.session.rollback()

    def save(self):
        try:
            self.put()
            self.commit()
        except Exception:
            self.rollback()
            raise

    def to_josn(self):
        pass

    def __json__(self):
        _d = {}
        if hasattr(self, '_json_cache') and self._json_cache:
            _d = self._json_cache
        for k, v in vars(self).items():
            print(k,v)
            if k.startswith('_'):
                continue
            if isinstance(v, datetime):
                v = v.strftime(default_datetime_format)
            if isinstance(v, date):
                v = v.strftime(default_date_format)
            _d[k] = v
        current_app.logger.info(vars(self).keys())
        if "dmp_user_id" in vars(self).keys():
            _d["dmp_user_name"] = self.users.dmp_username if self.users else "None"
        if "leader_dmp_user_id" in vars(self).keys():
            _d["leader_dmp_username"] = self.leader.dmp_username if self.leader else "None"
        if "approve_dmp_user_id" in vars(self).keys():
            _d["approve_dmp_username"] = self.approve_users.dmp_username
        if "submit_dmp_user_id" in vars(self).keys():
            _d["submit_dmp_username"] = self.submit_users.dmp_username
        if "dmp_database_id" in vars(self).keys():
            _d["dmp_database_name"] = self.database.dmp_database_name
        return _d

    def __repr__(self):
        return '####<%s %s> ' % \
               (self.__class__.__name__, self.__mapper__.primary_key[0].name)

    def __len__(self):
        return 1


class JSONEncoder(_json.JSONEncoder):
    def default(self, o):
        if isinstance(o, DMPModel):
            return o.__json__()
        return _json.JSONEncoder.default(self, o)


from .dmp_case import Case
from .dmp_data_table import DataTable
from .dmp_data_table_column import DataTableColumn
from .dmp_data_table_column_range import DataTableColumnRange
from .dmp_database import Database
from .dmp_form_add_data_table import FromAddDataTable
from .dmp_form_download import FromDownload
from .dmp_form_migrate import FromMigrate
from .dmp_form_upload import FromUpload
from .dmp_permission import Permissions
from .dmp_group import Groups
from .dmp_rights import Rights
from .dmp_user import Users
