#-*-coding:utf-8-*-
__author__ = 'SUNZHEN519'
import socket   #socket模块
import commands   #执行系统命令模块
import os
import threading
import sqlite3
import socket
import unittest
import time
import os
import HTMLTestRunner
s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #定义socket类型，网络通信，TCP
k=('127.0.0.1',8032)
s.bind(k)
s.listen(15)         #开始TCP监听
class MyThread(threading.Thread):
    def __init__(self, data):
        self.data=[i.strip()for i in  data.split('#')  if i.strip()!='']
        threading.Thread.__init__(self)
        self.tim=tim
    def run(self):
        #脚本地址
        suite1 = unittest.defaultTestLoader.discover(self.data[1], pattern="*.py", top_level_dir=None)
        suite=unittest.TestSuite([suite1])
        result_path=os.path.join(r"E:\HGTP_server\app\templates\result\\"+self.data[0]+'.html')
        now = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))  # 输出当前时间
        fp = open(result_path, 'wb')
        runner = HtmlTestRunner.HtmlTestRunner(stream=fp, title=u'用例执行情况', description=u'报告:')
        runner.run(suite)
        fp.close()
        db = sqlite3.connect(r'E:\HGTP_server\example.db')
        cu = db.cursor()
        time.sleep(1)
        cu.execute('update  run  set statu=0 where name="%s"' % self.data[0])
        db.commit()
        db.close()
while 1:
       name=None
       conn,addr=s.accept()   #接受TCP连接，并返回新的套接字与IP地址
       print'Connected by',addr    #输出客户端的IP地址
       kk=0
       tim=0
       data=conn.recv(1024)   #把接收的数据实例化
       ub=MyThread(data)
       ub.start()
                

