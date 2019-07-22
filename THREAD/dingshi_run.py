#-*-coding:utf-8-*-
__author__ = 'SUNZHEN519'
import socket   #socket模块
import commands   #执行系统命令模块
import os
import threading
import sqlite3
import socket
import time
import os
import unittest
import HtmlTestRunner
import smtplib
import json
import stat
from email.mime.text import MIMEText
import shutil
import urllib2
import urllib
class all_run(object):
 def __init__(self):
    while True:
     db = sqlite3.connect(r'C:\HGTP_server\example.db')
     cu = db.cursor()
     for i in cu.execute('select * from dingshi_run where statu="0" ' ).fetchall():
        if 'everyday' in i[2]:
           split_time=i[2].split('everyday')[-1]
             #转换为当天的时间
           run_time=time.strftime("%Y-%m-%d ", time.localtime(time.time()))+split_time
           shijianchuo_run=time.mktime(time.strptime(run_time, "%Y-%m-%d %H:%M"))
           if shijianchuo_run>time.time() :
               continue
           elif time.time()-float(shijianchuo_run)<=120 :
             cu.execute('update dingshi_run set last_run_time="%s" ,statu="1" where id=%s ' % (
               time.strftime("%Y-%m-%d", time.localtime(time.time())), int(i[6])))
             db.commit()
             #转化为文件命名的字符串，everyday+当天时间+id
             name_file='everyday'+str(time.time())+'#'+str(i[6])
             req = urllib2.Request('http://127.0.0.1:5021/run_hualala')
             data={}
             data['all_path']=i[3]
             data['email']=i[5]
             data['all_name']=i[0]
             data['run_time']=name_file
             data = urllib.urlencode(data)
             result = urllib2.urlopen(url=req, data=data)
             res = result.read()
             print 11111111111111
             print i
             print i[7]
             print run_time
             print  name_file
             print shijianchuo_run
        else:
           split_time=i[2].split(u'定时设置 ：')[-1].strip()
             #转换为当天的时间
           shijianchuo_run=time.mktime(time.strptime(split_time, "%Y-%m-%d %H:%M"))
           if shijianchuo_run > time.time():
                 continue
           elif time.time()-float(shijianchuo_run)<=120:
             #转化为文件命名的字符串，everyday+当天时间+id
             req = urllib2.Request('http://127.0.0.1:5021/run_hualala')
             print 7777777777
             run_time=time.strftime("%Y-%m-%d ", time.localtime(time.time())) + split_time
             name_file='today'+str(time.time())+'#'+str(i[6])
             data={}
             data['all_path']=i[3]
             data['email']=i[5]
             data['all_name']=i[0]
             data['run_time']=name_file
             data = urllib.urlencode(data)
             print name_file
             result = urllib2.urlopen(url=req, data=data)
             res = result.read()

     for i in cu.execute('select * from dingshi_run where statu="2" ' ).fetchall():

        if 'everyday' in i[2]:
          if  i[7].strip()==time.strftime("%Y-%m-%d", time.localtime(time.time())):
             continue
          else:
            split_time=i[2].split('everyday')[-1]
             #转换为当天的时间
            run_time=time.strftime("%Y-%m-%d ", time.localtime(time.time()))+split_time
            shijianchuo_run=time.mktime(time.strptime(run_time, "%Y-%m-%d %H:%M"))
          if shijianchuo_run > time.time():
                continue
          elif time.time()-float(shijianchuo_run)<=120:
             cu.execute('update dingshi_run set last_run_time="%s" ,statu="1" where id=%s ' % (
               time.strftime("%Y-%m-%d", time.localtime(time.time())), int(i[6])))
             db.commit()
             #转化为文件命名的字符串，everyday+当天时间+id
             name_file='everyday'+str(time.time())+'#'+str(i[6])
             req = urllib2.Request('http://127.0.0.1:5021/run_hualala')
             data={}
             data['all_path']=i[3]
             data['email']=i[5]
             data['all_name']=i[0]
             data['run_time']=name_file
             data = urllib.urlencode(data)
             result = urllib2.urlopen(url=req, data=data)
             res = result.read()



     db.close()
"""

         req = urllib2.Request('http://127.0.0.1:5021/run_hualala')
         data = {1: 2}
         data = urllib.urlencode(data)
         result = urllib2.urlopen(url=req, data=data)
         res = result.read()
     db.commit()
     db.close()
     req = urllib2.Request('http://127.0.0.1:5021/run_hualala')
     data={1:2}
     data = urllib.urlencode(data)
     result = urllib2.urlopen(url=req,data=data) # 发起GET http服务
     res = result.read() #把结果通过.read()函数读取出来
     """
if __name__=='__main__':
    all_run()
