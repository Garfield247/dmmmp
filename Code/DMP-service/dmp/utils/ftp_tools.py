#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/6/23
# @Author  : SHTD 


from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from dmp.extensions import celery


@celery.task
def ftp_server_hanlder(username, passwd, homedir, port):
    authorizer = DummyAuthorizer()
    authorizer.add_user(username=username, password=passwd, homedir=homedir)
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.passive_ports = range(2000, 4000)
    server = FTPServer(('0.0.0.0', port), handler)
    server.serve_forever()
