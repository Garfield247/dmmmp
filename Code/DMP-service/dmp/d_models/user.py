import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    """用户表"""
    __tablename_ = 'dmp_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    dmp_username = db.Column(db.String(32), unique=True, nullable=False, comment='用户名')
    real_name = db.Column(db.String(32), nullable=False, comment='真实姓名')
    email = db.Column(db.String(32), unique=True, nullable=False, comment='用户邮箱')
    passwd = db.Column(db.String(64), nullable=False, comment='用户密码，加密储存')
    confirmed = db.Column(db.Boolean, default=False, comment='用户激活状态')
    icon = db.Column(db.String(128), default=None, comment='用户头像')
    dmp_user_info = db.Column(db.String(256), default=None, comment='个人简介')
    last_login = db.Column(db.DateTime, default=datetime.datetime.now, comment='最后登录时间')
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    dmp_group_id = db.Column(db.Integer, db.ForeignKey('dmp_group.id'), nullable=False, comment='所属用户组ID，默认学生用户组')
    leader_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), comment='直属管理者，默认是超级管理员用户, 自关联')

    groups = db.relationship('Groups', backref='users')
    leader = db.relationship('Users', backref='leader')


class Group(db.Model):
    """用户组表"""
    __tablename_ = 'dmp_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户组ID')
    dmp_group_name = db.Column(db.String(32), unique=True, nullable=False, comment='用户组名')
    max_count = db.Column(db.Integer, comment='最大用户数量')
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')

    permissions = db.relationship('Permissions', secondary='dmp_group_permission', backref='permission_groups')
    rights = db.relationship('Rights', secondary='dmp_group_rights', backref='rights_group')


class Permissions(db.Model):
    """权限表"""
    __tablename__ = 'dmp_permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='权限ID')
    route = db.Column(db.String(64), nullable=False, comment='权限路由')
    dmp_permission_name = db.Column(db.String(32), nullable=False, comment='路由功能名称')


class GroupPermission(db.Model):
    """用户组_权限表"""
    __tablename__ = 'dmp_group_permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_group_id = db.Column(db.Integer, db.ForeignKey('dmp_group.id'), nullable=False, comment='用户组ID')
    dmp_permission_id = db.Column(db.Integer, db.ForeignKey('dmp_permission.id'), comment='权限ID')


class Rights(db.Model):
    """权利表"""
    __tablename__ = 'dmp_rights'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='功能ID')
    dmp_rights_name = dmp_permission_name = db.Column(db.String(32), nullable=False, comment='路由功能名称')


class GroupRights(db.Model):
    """用户组权利表"""
    __tablename__ = 'dmp_group_rights'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_rights_id = db.Column(db.Integer, db.ForeignKey('dmp_rights.id'), nullable=False, comment='权限ID')
    dmp_group_id = db.Column(db.Integer, db.ForeignKey('dmp_group.id'), nullable=False, comment='用户组ID')
