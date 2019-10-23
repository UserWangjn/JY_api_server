# uncompyle6 version 3.3.4
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02)
# [GCC 9.1.0]
# Embedded file name: C:\jieyuelianhe\old_all_server\HGTP_server\fileconfig.py
# Compiled at: 2019-03-18 13:47:24
import os, socket
SECRET_KEY = 'you-will-never-guess'
basedir = os.path.abspath(os.path.dirname(__file__))
DBPATH = os.path.join(basedir, '..', 'db')

parent_path = os.path.dirname(basedir)
myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DBPATH, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
JIAO_DIZHI = '../s_ben'
MOBANDIZHI = 'mulu44.py'
GENMULU = '../web'
SOCKET = 8022
JIEGUO = '../web//templates/'
DB_DIZHI = os.path.join(DBPATH, 'example.db')
CSRF_ENABLED = True
RESULT = 'web/app/templates/result'
PERMANENT_SESSION_LIFETIME = 600
LOG = os.path.join(basedir, 'log.txt')
JIE_KOU_URL = '../lr_test'
LOCUST_FILE = '../locust_file'
ALLRUN_FILE = os.path.join(parent_path, 'run_mulu')
JIE_KOU = os.path.join(DBPATH, 'jiekou.db')
BENJI_IP = ('10.50.180.55', 8065)
SERVER_DI = parent_path
GIT_FILE_MULU = os.path.join(parent_path, 'GIT_FILE_MULU')
FILE_CASE = os.path.join(basedir, 'app/static/tongji_num')
RESULT_PICT_SAVE = os.path.join(basedir, 'app/static/result_pic')
LOG_FILE = '/static/log_pic'
BASEDIR = os.path.join(basedir, 'app/static/log_pic')
LOCAL_SERVER_PORT = '5041'
NUM_JISHU = 0
MOCK_DIZHI = os.path.join(DBPATH, 'dangban_server.db')
MOCK_URL = 'mock_return'
APPIUM_IP = '10.50.180.56:5000'
JMETER_LOG = os.path.join(DBPATH, 'jmeter_get.db')
JMETER_IP = '192.168.75.35:8889'
PHONE_DB = os.path.join(DBPATH, 'phone_detail.db')
ZICHAN_QUANXIAN = 'yanxuelie,guochen,chensiyu'
PHONE_FILE = os.path.join(parent_path, 'phone_file')
PHONE_FILE_DOWNLOAD = os.path.join(parent_path, 'phone_file_download')