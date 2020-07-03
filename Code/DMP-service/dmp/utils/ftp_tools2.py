#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/6/23
# @Author  : SHTD 

#   user    passwd  homedir         path
#   neo     123456  /home/neo/data  elradfmwM
ip = "0.0.0.0"
port = 21
max_upload = 300 * 1024
max_download = 300 * 1024
max_cons = 256
max_pre_ip = 10
passive_ports = (2223, 2233)
enable_anonymous = False
enable_logging = True
logging_name = r"pyftp.log"
masquerade_address = ""
welcome_banner = r"Welcome to private ftp."
anonymous_path = r"/tmp"

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import ThrottledDTPHandler
from pyftpdlib.handlers import FTPHandler
import logging


def init_ftp_server():
    authorize = DummyAuthorizer()
    """
            读权限:
             - "e" = 改变文件目录
             - "l" = 列出文件 (LIST, NLST, STAT, MLSD, MLST, SIZE, MDTM commands)
             - "r" = 从服务器接收文件 (RETR command)

            写权限:
             - "a" = 文件上传 (APPE command)
             - "d" = 删除文件 (DELE, RMD commands)
             - "f" = 文件重命名 (RNFR, RNTO commands)
             - "m" = 创建文件 (MKD command)
             - "w" = 写权限 (STOR, STOU commands)
             - "M" = 文件传输模式 (SITE CHMOD command)
    """
    # # 日志记录
    if enable_logging:
        logging.basicConfig(filename="pyftp.log", level=logging.INFO)
    # 匿名登录
    if enable_anonymous:
        authorize.add_anonymous(anonymous_path)
    # 读取用户信息登录
    for user in user_list:
        name, passwd, homedir, permit = user
        try:
            authorize.add_user(name, passwd, homedir, perm=permit)
        except:
            print("user info config error. %s", user[0])
            exit(2)

    # 限制ftp用户读写速度
    dtl_handler = ThrottledDTPHandler
    dtl_handler.read_limit = max_download
    dtl_handler.write_limit = max_upload

    # 服务器配置信息
    handler = FTPHandler
    handler.authorizer = authorize
    handler.banner = welcome_banner
    handler.passive_ports = passive_ports
    handler.masquerade_address = masquerade_address

    address_port = (ip, port)
    server = FTPServer(address_port, handler=handler)
    server.max_cons = max_cons
    server.max_cons_per_ip = max_pre_ip
    server.serve_forever()


def init_conf_file(text):
    for x, item in enumerate(text):
        if item == "#":
            return text[:x]
        pass
    return text


def init_user_listconf():  #
    try:
        f = open('baseftp.ini', encoding='utf-8')
    except:
        print("baseftp open error.")
        exit(1)
    while 1:
        line = f.readline()
        if len(init_conf_file(line)) > 3:
            user_list.append(line.split())
        if not line:
            break
    f.close()


if __name__ == '__main__':
    user_list = []
    init_user_listconf()
    init_ftp_server()
