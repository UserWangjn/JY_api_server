# -*-coding:utf-8-*-
__author__ = 'SUNZHEN519'
import socket  # socket模块
import commands  # 执行系统命令模块
import os
import threading
import sqlite3
import socket
import json
import time
import smtplib
from email.mime.text import MIMEText
import os
import unittest
import HTMLTestRunner
result_path = os.path.join(r"C:\all_new\result_mulu",str(time.time())+'.html', )
now = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))  # 输出当前时间
fp = open(result_path, 'wb')
runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'用例执行情况', description=u'报告:')
runner.run(unittest.defaultTestLoader.discover(r"C:\all_new\run_mulu\git\1505985874.94", pattern="*.py",top_level_dir=None))
fp.close()
db = sqlite3.connect(r'C:\all_new\HGTP_server\example.db')
cu = db.cursor()
cu.executemany('update  dingshi_run  set run_result=? where id =?',
               [(json.dumps(HTMLTestRunner.all_detail),'267'.split('#')[-1])])

db.commit()
db.close()








