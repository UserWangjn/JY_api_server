# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import os
SECRET_KEY = 'you-will-never-guess'
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
#脚本存储路径
JIAO_DIZHI=r'C:\s_ben'
#运行模板文件存放路径名为mulu44.py
MOBANDIZHI=r'C:\web flask\mulu44.py'
GENMULU=r'C:\web flask'
SOCKET=8022
#生成结果文件html的地址
JIEGUO=r'C:\web flaskapp\templates\\'
#数据库example地址
DB_DIZHI=r'C:\all_new\HGTP_server\example.db'
CSRF_ENABLED = True
#生成结果文件存放目录
RESULT=r'C:\web flask\app\templates\result'
PERMANENT_SESSION_LIFETIME=600
LOG=os.path.join(basedir, 'log.txt')
#接口url
JIE_KOU_URL=r'C:\work\lr_test'
LOCUST_FILE=r'C:\all_new\locust_file'
#哗啦啦运行脚本存放地方
ALLRUN_FILE=r'C:\all_new\run_mulu'
#接口运行数据库
JIE_KOU=r'C:\all_new\HGTP_server\jiekou.db'
#本机ip地址
BENJI_IP=('192.168.18.129',8065)