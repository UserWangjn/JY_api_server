# -*-coding:utf-8-*-
__author__ = 'SUNZHEN519'
import socket  # socket模块
import commands  # 执行系统命令模块
import os
import threading
import sqlite3
import socket
import time
import smtplib
from email.mime.text import MIMEText
import os
import unittest
import HtmlTestRunner
result_path = os.path.join(r"C:\result_mulu", 'flask\\' +'1505371098.79'+ '.html')
now = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))  # 输出当前时间
fp = open(result_path, 'wb')
runner = HtmlTestRunner.HtmlTestRunner(stream=fp, title=u'用例执行情况', description=u'报告:')
runner.run(unittest.defaultTestLoader.discover(r"C:\run_mulu\flask\1505371098.8", pattern="*.py",top_level_dir=None))
fp.close()
with open(r'F:\22.txt', 'a') as  f:
    runner = unittest.TextTestRunner(stream=f, verbosity=2)







