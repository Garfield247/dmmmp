# -*- coding: utf-8 -*-
# @Date    : 2020/8/19
# @Author  : SHTD

from dmp.extensions import db
from dmp.models import DMPModel


class {TABLENAE}(db.Model, DMPModel):
    """  """
    __tablename__ = ''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='')
