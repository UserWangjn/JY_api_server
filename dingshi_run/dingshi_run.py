import socket   #socket模块
import subprocess   #执行系统命令模块
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
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import os
import signal
import sys
from fileconfig import DB_DIZHI
class all_run(object):
 def __init__(self):
    mulu = DB_DIZHI
    print(os.path.abspath(mulu))
    print(__name__)
    print('=============================')
    run_mulu=os.path.join(os.path.dirname(os.getcwd()),'run_mulu')
    db = sqlite3.connect(mulu)
    cu = db.cursor()
    while True:
     db = sqlite3.connect(mulu)
     cu = db.cursor()
     if len(cu.execute('select * from dingshi_run where statu="1" ').fetchall())==0 and int(time.time())%60<10:
           for dirpath, dirnames, filenames in os.walk(run_mulu):
             for file in filenames:
                 fullpath = os.path.join(dirpath, file)
                 if os.path.isfile(fullpath):
                     os.chmod(fullpath, stat.S_IWRITE)
                     os.remove(fullpath)
                     print(fullpath + " removed!")
           files = os.listdir(run_mulu)
           for file in files:
             child_file = os.listdir(os.path.join(run_mulu, file))
             for z in child_file:
                 m = os.path.join(run_mulu, file,z)
                 try:
                   shutil.rmtree(m)
                 except:
                     pass
           # pids = psutil.pids()
           # for pid in pids:
           #      try:
           #         p = psutil.Process(pid)
           #         if 'chromedriver' in p.name() or 'WerFault' in p.name() or 'chrome' in p.name():
           #           print  p.name()
           #           os.system('TASKKILL /F /IM ' + p.name())
           #      except:
           #          pass
     #如果没有运行自动化则是杀死程序
     for i in cu.execute('select * from dingshi_run where statu="0" ' ).fetchall():
       if '实时' not in i[2]:
        if 'everyday' in i[2]:
           split_time=i[2].split('everyday')[-1]
             #转换为当天的时间
           run_time=time.strftime("%Y-%m-%d ", time.localtime(time.time()))+split_time
           shijianchuo_run=time.mktime(time.strptime(run_time, "%Y-%m-%d %H:%M"))
           if shijianchuo_run>time.time():
               continue
           elif time.time()-float(shijianchuo_run)<=120 :
             cu.execute('update dingshi_run set last_run_time="%s" ,statu="1" where id=%s ' % (
               time.strftime("%Y-%m-%d", time.localtime(time.time())), int(i[6])))
             db.commit()
             #转化为文件命名的字符串，everyday+当天时间+id
             id=str(i[6])
             req = urllib.request.Request('http://127.0.0.1:5025/run_hualala')
             data={}
             data['all_path']=i[3]
             email_detail=json.loads(i[5])
             data['email']=email_detail['receive']
             data['emali_title'] = email_detail['title'].encode('utf-8')
             data['send_email_user'] = email_detail['send']
             data['all_name']=i[0]
             data['id']=id
             data['name']=i[0]
             data['job_id'] = json.loads(i[10])['job_id']
             data['statu']='jiekou_dingshi'
             data['all_branch'] = i[9]
             data['job'] = i[10]
             data['run_server'] = 'Automatic distribution'
             data = urllib.parse.urlencode(data)
             result = urllib.request.urlopen(url=req, data=data)
             res = result.read()
        else:
           split_time=i[2].split('定时设置 ：')[-1].strip()
             #转换为当天的时间
           shijianchuo_run=time.mktime(time.strptime(split_time, "%Y-%m-%d %H:%M"))
           if shijianchuo_run > time.time():
                 continue
           elif time.time()-float(shijianchuo_run)<=120:
             cu.execute('update dingshi_run set last_run_time="%s" ,statu="1" where id=%s ' % (
                   time.strftime("%Y-%m-%d", time.localtime(time.time())), int(i[6])))
             db.commit()
             #转化为文件命名的字符串，everyday+当天时间+id
             req = urllib.request.Request('http://127.0.0.1:5025/run_hualala')
             run_time=time.strftime("%Y-%m-%d ", time.localtime(time.time())) + split_time
             id=str(i[6])
             data={}
             data['all_path']=i[3]
             email_detail = json.loads(i[5])
             data['email'] = email_detail['receive']
             data['send_email_user'] = email_detail['send']
             data['all_name']=i[0]
             data['id']=id
             data['emali_title'] = email_detail['title'].encode('utf-8')
             data['name'] = i[0]
             data['statu'] = 'jiekou_dingshi'
             data['all_branch'] = i[9]
             data['job'] = i[10]
             data['run_server'] = 'Automatic distribution'
             data['job_id']=json.loads(i[10])['job_id']
             data = urllib.parse.urlencode(data)
             result = urllib.request.urlopen(url=req, data=data)
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
             id=str(i[6])
             req = urllib.request.Request('http://127.0.0.1:5025/run_hualala')
             data={}
             data['all_path']=i[3]
             email_detail = json.loads(i[5])
             data['email'] = email_detail['receive']
             data['send_email_user'] = email_detail['send']
             data['all_name']=i[0]
             data['id']=id
             data['job_id'] = json.loads(i[10])['job_id']
             data['emali_title'] = email_detail['title'].encode('utf-8')
             data['name'] = i[0]
             data['statu'] = 'jiekou_dingshi'
             data['all_branch'] = i[9]
             data['job'] = i[10]
             data['run_server'] ='Automatic distribution'
             data = urllib.parse.urlencode(data)
             result = urllib.request.urlopen(url=req, data=data)
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
#if __name__=='__main__':
#    all_run()
