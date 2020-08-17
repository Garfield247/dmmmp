#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD
import os
import json
import datetime
from flask_script import Manager, Server
from flask_migrate import MigrateCommand

from dmp import create_app
from dmp.extensions import db

# 创建命令起动控制对象

# 获取配置
config_name = os.environ.get('DMP_CONFIG') or 'testing'

# 创建实例
app = create_app(config_name)
manager = Manager(app)
# 添加数据库迁移命令
manager.add_command('db', MigrateCommand)
# 添加服务配置


manager.add_command('runserver', Server(host='0.0.0.0', port=7789,use_debugger=True))


# 路由列表命令
@manager.command
def url_map():
    permission_list = [{"route": r.rule, "desc": None if not r.defaults else r.defaults.get("desc")} for r in
                       app.url_map.__dict__.get("_rules")]
    for per in permission_list:
        app.logger.info(per)


# 删除所有表
@manager.command
def drop_db():
    app.logger.info("drop db")
    db.drop_all()


# 创建所有表
@manager.command
def create_db():
    app.logger.info("create db")
    db.create_all()


# 生成数据表测试数据
@manager.command
def create_test_db_table_data():
    import random
    from dmp.models import Users, Case, Database
    from dmp.api.dbtable import post

    count = 30
    for i in range(count):
        new_test_table = post(
            dmp_data_table_name="dmp_test_dbtable_%d" % i,
            db_table_name="dmp_test_db_table_name%d" % i,
            description="测试表",
            dmp_user_id=random.choice(Users.query.all()).id,
            dmp_database_id=random.choice(Database.query.all()).id,
            dmp_case_id=random.choice(Case.query.all()).id
        )

        app.logger.info("add test data :" + str(new_test_table))

        app.logger.info("add test data :" + str(new_test_table))


# 初始化
@manager.command
def sys_init():
    # db.drop_all()
    # db.create_all()
    from dmp.models import Permissions
    Permissions.init_permission()
    from dmp.models import Groups
    Groups.init_group()
    # from dmp.models import Users
    # Users.create_test_user()


@manager.command
def test_datax():
    from dmp.test.datax_test import test_csv2mysql,test_csv2hive,test_hive2csv
    test_hive2csv()

    # from dmp.models import Users
    # Users.create_test_user()

@manager.command
def sqla():
    from dmp.models import Forms,FormUpload,FormMigrate,FormDownload,FormAddDataTable
    from dmp.extensions import db
    # print(dir(DataTable))
    ta = json.load(open("/Users/catman/Desktop/dmp_from_add_data_table.json", "r"))
    tm = json.load(open("/Users/catman/Desktop/dmp_from_migrate.json", "r"))
    tu = json.load(open("/Users/catman/Desktop/dmp_from_upload.json", "r"))
    td = json.load(open("/Users/catman/Desktop/dmp_from_download.json", "r"))
    for a in tu.get("RECORDS"):
        new_form_info = FormUpload(


            filetype=a.get("filetype"),
            filepath=a.get("filepath"),
            column_line=a.get("column_line"),
            column=a.get("column"),
            method=a.get("method"),
            destination_dmp_database_id=a.get("destination_dmp_database_id"),
            destination_db_table_name=a.get("destination_db_table_name"),
            dmp_case_id=a.get("dmp_case_id"),
            dmp_data_table_name=a.get("dmp_data_table_name"),

        )
        new_form_info.save()
        new_form = Forms(
            form_info_id=new_form_info.fid,
            submit_dmp_user_id=a.get("submit_dmp_user_id"),
            submit_on = datetime.datetime.strptime(a.get("submit_on"), "%d/%m/%Y %H:%M:%S") if a.get("submit_on") else None,
            description = a.get("description"),
            approve_dmp_user_id = a.get("approve_dmp_user_id",1) if a.get("approve_dmp_user_id",1).strip() else None,
            approve_on = datetime.datetime.strptime(a.get("approve_on"), "%d/%m/%Y %H:%M:%S") if a.get(
                "approve_on") else None,
            approve_result = a.get("approve_result"),
            answer = a.get("answer"),
            created_on = datetime.datetime.strptime(a.get("created_on"), "%d/%m/%Y %H:%M:%S") if a.get(
                "created_on") else None,
            changed_on = datetime.datetime.strptime(a.get("changed_on"), "%d/%m/%Y %H:%M:%S") if a.get(
                "changed_on") else None,
            form_type = a.get("form_type"),
            # finish = a.get("finish"),
            # result = a.get("result"),
        )
        new_form.save()



@manager.option("-id",dest="pid")
def test_per(pid):
    from dmp.api.form import form_permission
    res = form_permission(pid)
    print(res)



@manager.option('-n', '-dmp_username', dest='dmp_username')
@manager.option('-r', '-real_name', dest='real_name')
@manager.option('-p', '-passwd', dest='passwd')
@manager.option('-e', '-email', dest='email')
def createsuperuser(dmp_username, real_name, passwd, email):
    """创建管理员用户"""
    from dmp.models import Users, Groups
    from dmp.utils.ep_data import EnvelopedData
    if not all([dmp_username, real_name, passwd, email]):
        return 'Insufficient parameter, please recreate superuser.'

    db_user_count = Users.query.count()
    if db_user_count == 0:
        user = Users(dmp_username=dmp_username, real_name=real_name, password=passwd, email=email)
        rootgroup = Groups.query.filter(Groups.id == 1).first()
        user.dmp_group_id = 1
        user.leader_dmp_user_id = None
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        res = EnvelopedData.create_root(rootgroup)
        if isinstance(res, str):
            return {'msg': res}
        return {'msg': 'Super administrator has been created successfully.'}
    else:
        return {'msg': 'The super administrator already exists in the database, please do not add it again.'}


if __name__ == '__main__':
    manager.run()
