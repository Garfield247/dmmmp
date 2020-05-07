import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Database(db.Model):
    """数据库表"""
    __tablename__ = 'dmp_database'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_database_name = db.Column(db.String(32), unique=True, nullable=False, comment='数据显示名称')
    db_type = db.Column(db.Integer, nullable=False, comment='数据库类型,hive:0,mysql:1,mongo:2')
    db_host = db.Column(db.String(32), nullable=False, comment='数据库主机地址')
    db_port = db.Column(db.Integer, nullable=False, comment='数据库端口号')
    db_name = db.Column(db.String(32), comment='数据库名称')
    db_username = db.Column(db.String(32), comment='数据库用户名')
    db_passwd = db.Column(db.String(64), comment='数据库密码')
    description = db.Column(db.String(128), comment='数据库说明')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), nullable=False, comment='所属用户ID')

    users = db.relationship('Users', backref='database')


class DataCase(db.Model):
    """案例表"""
    __tablename__ = 'dmp_data_case'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_case_name = db.Column(db.String(32), nullable=False, comment='案例名称')
    description = db.Column(db.String(128), comment='案例说明')
    url_name = db.Column(db.String(32), comment='可视化网站名称')
    url = db.Column(db.String(64), comment='网址')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')


class DataTable(db.Model):
    """数据表"""
    __tablename__ = 'dmp_data_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_data_table_name = db.Column(db.String(32), unique=True, nullable=False, comment='数据名称')
    db_table_name = db.Column(db.String(32), nullable=False, comment='数据库内数据表名称')
    description = db.Column(db.String(128), comment='数据说明')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), nullable=False, comment='添加人')
    dmp_database_id = db.Column(db.Integer, db.ForeignKey('dmp_database.id'), nullable=False, comment='数据库ID')
    dmp_data_case_id = db.Column(db.Integer, db.ForeignKey('dmp_data_case.id'), nullable=False, comment='所属案例ID')

    users = db.relationship('Users', backref='users_datatable')
    database = db.relationship('Database', backref='database_datatable')
    datacase = db.relationship('DataCase', backref='datacase_datatable')


class DataTableColumn(db.Model):
    """数据列信息表"""
    __tablename__ = 'dmp_data_table_column'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_data_table_column_name = db.Column(db.String(32), nullable=False, comment='列名')
    groupby = db.Column(db.Boolean, default=False, comment='可以进行分组')
    wherein = db.Column(db.Boolean, default=False, comment='可以区间筛选')
    isdate = db.Column(db.Boolean, default=False, comment='是否为时间日期字段')
    description = db.Column(db.String(128), comment='字段说明')
    dmp_data_table_id = db.Column(db.Integer, db.ForeignKey('dmp_data_table.id'), nullable=False, comment='数据ID')

    datatable = db.relationship('DataTable', backref='data_table_column')


class TableColumnRange(db.Model):
    """数据列区间表"""
    __tablename__ = 'dmp_table_column_range'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    context = db.Column(db.String(256), comment='内容')
    dmp_data_table_column_id = db.Column(db.Integer, db.ForeignKey('dmp_data_table_column.id'), nullable=False,
                                         comment='列ID')

    data_table_column = db.relationship('DataTableColumn', backref='table_column_range')


class FromAddDataTable(db.Model):
    """数据从数据库添加表单表"""
    __tablename__ = 'dmp_from_add_data_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_data_table_name = db.Column(db.String(64), unique=True, comment='数据名称')
    db_table_name = db.Column(db.String(32), nullable=False, comment='数据库内数据表名称')
    submit_on = db.Column(db.DateTime, nullable=False, comment='提交时间')
    description = db.Column(db.String(128), comment='说明')
    approve_on = db.Column(db.DateTime, comment='审批时间')
    approve_result = db.Column(db.Integer, comment='审批结果,默认:0,通过:1,不通过:2')
    answer = db.Column(db.String(32), comment='审批答复')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    submit_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), nullable=False, comment='提交人')
    dmp_database_id = db.Column(db.Integer, db.ForeignKey('dmp_database.id'), nullable=False, comment='数据库ID')
    dmp_case_id = db.Column(db.Integer, db.ForeignKey('dmp_data_case.id'), nullable=False, comment='所属案例ID')
    approve_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), comment='审批人')

    submit_users = db.relationship('Users', backref='submitusers_from_add_data_table')
    approve_users = db.relationship('Users', backref='approveusers_from_add_data_table')
    database = db.relationship('Database', backref='database_from_add_data_table')
    datacase = db.relationship('DataCase', backref='datacase_from_add_data_table')


class FromUpload(db.Model):
    """数据文件上传表单表"""
    __tablename__ = 'dmp_from_upload'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filetype = db.Column(db.Integer, nullable=False, comment='文件类型')
    filepath = db.Column(db.String(128), nullable=False, comment='文件路径')
    column_line = db.Column(db.Integer, comment='列名行号')
    column = db.Column(db.String(32), comment='自定义列名')
    json_dimension_reduction = db.Column(db.Boolean, comment='json数据是否遍历存储')
    new_table_name = db.Column(db.String(32), nullable=False, comment='表名')
    method = db.Column(db.String(32), nullable=False, comment='新建、添加或覆盖')
    description = db.Column(db.String(128), comment='说明')
    submit_on = db.Column(db.DateTime, nullable=False, comment='提交时间')
    approve_on = db.Column(db.DateTime, comment='审批时间')
    approve_result = db.Column(db.Integer, comment='审批结果,默认:0,通过:1,不通过:2')
    answer = db.Column(db.String(32), comment='审批答复')
    upload = db.Column(db.Boolean, comment='是否成功')
    upload_result = db.Column(db.String(32), comment='数据上传结果')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    submit_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), nullable=False, comment='提交人')
    destination_dmp_database_id = db.Column(db.Integer, db.ForeignKey('dmp_database.id'), nullable=False,
                                            comment='目标数据库ID')
    dmp_data_case_id = db.Column(db.Integer, db.ForeignKey('dmp_data_case.id'), nullable=False, comment='所属案例')
    approve_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), comment='审批人')

    submit_users = db.relationship('Users', backref='submitusers_from_upload')
    approve_users = db.relationship('Users', backref='approveusers_from_upload')
    database = db.relationship('Database', backref='database_from_upload')
    datacase = db.relationship('DataCase', backref='datacase_from_upload')


class FromMigrate(db.Model):
    """数据迁移表单表"""
    __tablename__ = 'dmp_from_migrate'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rule = db.Column(db.String(64), comment='数据库提取规则')
    new_table_name = db.Column(db.String(32), nullable=False, comment='新表名')
    method = db.Column(db.String(32), nullable=False, comment='新建、覆盖或添加')
    description = db.Column(db.String(128), comment='说明')
    submit_on = db.Column(db.DateTime, nullable=False, comment='提交时间')
    approve_on = db.Column(db.DateTime, comment='审批时间')
    approve_result = db.Column(db.Integer, comment='审批结果,默认:0,通过:1,不通过:2')
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

    submit_users = db.relationship('Users', backref='submitusers_from_migrate')
    approve_users = db.relationship('Users', backref='approveusers_from_migrate')
    datatable = db.relationship('DataTable', backref='datatable_from_migrate')
    database = db.relationship('Database', backref='database_from_migrate')


class FromDownload(db.Model):
    """数据下载表单表"""
    __tablename__ = 'dmp_from_download'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rule = db.Column(db.String(64), comment='数据库提取规则')
    description = db.Column(db.String(128), comment='说明')
    submit_on = db.Column(db.DateTime, nullable=False, comment='提交时间')
    approve_on = db.Column(db.DateTime, comment='审批时间')
    approve_result = db.Column(db.Integer, comment='审批结果,默认:0,通过:1,不通过:2')
    answer = db.Column(db.String(32), comment='审批答复')
    ftp_url = db.Column(db.String(64), comment='FTP下载链接')
    ftp_pid = db.Column(db.Integer, comment='FTP进程号')
    filepath = db.Column(db.String(128), comment='文件路径')
    finish = db.Column(db.Boolean, comment='是否完成')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    submit_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), nullable=False, comment='提交人')
    dmp_data_table_id = db.Column(db.Integer, db.ForeignKey('dmp_data_table.id'), nullable=False, comment='源数据表ID')
    approve_dmp_user_id = db.Column(db.Integer, db.ForeignKey('dmp_user.id'), comment='审批人')

    submit_users = db.relationship('Users', backref='submitusers_from_download')
    approve_users = db.relationship('Users', backref='approveusers_from_migrate')
    datatable = db.relationship('DataTable', backref='datatable_from_download')
