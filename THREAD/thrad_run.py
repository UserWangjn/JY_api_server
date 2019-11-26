import socket   #socket模块
import subprocess   #执行系统命令模块
import os
import threading
import sqlite3
import socket
import time
import urllib.request, urllib.parse, urllib.error
from .jie_kou_test.pi_run import *
import os
import unittest
import jenkins
import HtmlTestRunner
import smtplib
import json
import stat
import urllib.request, urllib.error, urllib.parse
from .jie_kou_test.pi_run import all_run
from email.mime.text import MIMEText
import socket
import random
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import shutil
import requests
from fileconfig import basedir

#调用http接口，设置运行状态
def run_statu_change(statu,data,ip):
    data=urllib.parse.urlencode({'statu':statu,'data':data})
    url = 'http://' + ip + ':5025/change_run_statu'
    req=urllib.request.Request(url=url, data=data)
    while True:
        try:
             res_data = urllib.request.urlopen(req).read()
        except:
            pass
        else:
            break
    return res_data
def send_emali(name, id,email_detail,server_di,server_ip,run_statu,pic_mulu):
    email_detail=email_detail
    #email_address = [i for i in run_statu_change('email',name,server_ip).split('##') if i.strip() != ''][0]
    data=json.dumps({'name':name,'send_email':email_detail['send']})
    fajianren_detail=run_statu_change('email',data,server_ip)
    email_address=[i for i in email_detail['receive'].split('##') if i.strip()!=''  ]
    if len(email_address) == 0:
        return "just"
    sender = email_detail['send']
    smtpserver = 'mail.hualala.com'
    username = email_detail['send']
    if '(time)' in email_detail['title']:
        title=email_detail['title'].replace('(time)',time.strftime("%Y年%m月%d日", time.localtime()))
    else:
         title=email_detail['title']
    subject = title.decode('utf-8')
    #password = 'qwer1234!@#$'
    password=json.loads(fajianren_detail)['data'][1]
    params={'statu':'email'}
    msg = MIMEMultipart('related')
    if '各业务线本地使用统计'  in email_detail['title']:
        test_parm={'name':str(int(time.time()))}
        print(7777777777777777777777777777777777777777777777777777)
        print('http://'+server_ip+':5025/tongji_mail')
        print(test_parm)
        html = requests.get('http://'+server_ip+':5025/tongji_mail',params=test_parm).text
    elif 'jiekou'  in run_statu:
        html = requests.get('http://'+server_ip+':5025/jiekou_result/' + str(id),params=params).text
    else:
         html=requests.get('http://'+server_ip+':5025/dingshi_result/'+str(id),params=params).text
    msg.attach( MIMEText(html, 'html', 'utf-8'))
    msg['Subject'] = subject
    if '各业务线本地使用统计' not  in email_detail['title']:
        file = open(os.path.join(pic_mulu,str(id)+'.png'), "rb")
        img_data = file.read()
        file.close()
        img = MIMEImage(img_data)
        img.add_header('Content-ID', '<image1>')
        msg.attach(img)
    else:
        tongji_mullu=os.path.join(os.path.dirname(pic_mulu),'log_pic',test_parm['name']+'local_today_email.png')
        file = open(tongji_mullu, "rb")
        img_data = file.read()
        file.close()
        img = MIMEImage(img_data)
        img.add_header('Content-ID', '<image1>')
        msg.attach(img)

    smtp  = smtplib.SMTP_SSL("smtp.jieyuechina.com",port=465)
    smtp.login(username, password)
    msg['From'] = email_detail['send']
    receiver=[i for i in email_detail['receive'].split('##') if i.strip() != '']
    msg['To'] = receiver[0]
    smtp.sendmail(sender, receiver, msg.as_string())
    return 'send_success'
#根据传过来的目录找到下面的目录，然后往上找父目录，三级，正确目录，参数为接口传过来的目录
def jiekou_path(path,all_git):
    jiekou_path=[]
    for dirpath, dirnames, filenames in os.walk(path):
        for file in dirnames:
            if '.git'  not in os.path.join(dirpath, file) and 'json.txt' in  os.listdir(os.path.join(dirpath, file)):
                git_base_name=os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(dirpath)))))
                s=dirpath
                while True:
                    git_base_name = os.path.basename(s)
                    if s==os.path.dirname(s):
                        break
                    if git_base_name not in list(all_git.keys()):
                        s = os.path.dirname(s)
                        continue
                    else:
                        break
                jiekou_path.append([os.path.join(dirpath, file),all_git[git_base_name]])
    return jiekou_path
#批量运行接口测试
def piliang_run(data,all_git):
    data=json.loads(data)
    all_run.run(jiekou_path(data['run_dir'],all_git), time.time(), data['server_ip'],data['id'],data['run_id'])
    #发送结束请求[
    # url='http://'+data['server_ip']+':5025/piliang_run_git_over'
    # test_data = urllib.urlencode({'statu':'over','id':data['id'],'ip':data['server_ip']})
    # req = urllib2.Request(url=url, data=test_data)
    # res_data = urllib2.urlopen(req).read()
class MyThread(threading.Thread):
    def __init__(self, data):
        self.data=json.loads(data)
        threading.Thread.__init__(self)
    def run(self):
        #脚本地址
        time0=time.time()
        run_dir = os.path.join(basedir,'run')
        if os.path.exists(run_dir):
            for i in [os.path.join(run_dir, i) for i in os.listdir(run_dir)]:
                os.chmod(i, stat.S_IWRITE)
                if os.path.isdir(i):
                    shutil.rmtree(i)
                else:
                   os.remove(i)
        run_path=os.path.join(run_dir, self.data['name']+os.path.basename(self.data['run_dir'])+'.py')
        print(self.data['id'])
        id=str(self.data['id'])
        #删除结果文件
        if self.data['statu'] != 'jiekou_shishi':
            run_db_mo=os.path.join(self.data['server_di'],'example.db')
        run_statu_change('running',self.data['id'],self.data['server_ip'])
        email_detail=json.loads(self.data['email_detail'])
        #运行job
        job=json.loads(self.data['job'])
        zidong_statu='SUCCESS'
        if job['name'].strip()!='no select'  and self.data['job_id'].strip()!='':
            jobs=run_statu_change('jekins', json.dumps({'job_name':job['name'],'job_id':self.data['job_id'],'user_name':self.data['name']}), self.data['server_ip'])
            jobs=json.loads(jobs)['data']

            jenkins_server_url=jobs[-3].strip()
            user_id=jobs[0].strip()
            api_token=jobs[2].strip()
            server = jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token)
            job_name = jobs[3].strip()
            num = server.get_job_info(job_name)['lastBuild']['number']
            server.build_job(job_name,parameters=json.loads(jobs[-1]))
            while True:
                if server.get_job_info(job_name)['lastBuild']['number'] - 1 == num:
                    num = server.get_job_info(job_name)['lastBuild']['number']
                    break
            time.sleep(1)
            while server.get_build_info(job_name, num)['building']:
                time.sleep(1)
            result=job
            result['result']=server.get_build_info(job_name, num)['result']
            zidong_statu=result['result']
            result=json.dumps({'id':self.data['id'],'result':result})
            run_statu_change('job_result', result, self.data['server_ip'])
        if zidong_statu=='SUCCESS':
            if self.data['statu'] not in ['jiekou_shishi','jiekou_dingshi']:
                s = open(run_path, 'w')
                id = str(self.data['id'])
                s.write(open(os.path.join(basedir, 'model.py'), 'r').read().replace('##', str(self.data['id'])).replace('%%', self.data['run_dir'].encode('gb2312')).replace('***', run_db_mo.encode('gb2312')))
                s.close()
                os.system('python '+run_path)
                for parent, dirnames, filenames in os.walk(self.data['run_dir']):
                    for filename in filenames:
                        os.chmod(os.path.join(parent, filename), stat.S_IWRITE)
            elif self.data['statu'] == 'jiekou_shishi' or self.data['statu']=='jiekou_dingshi':
                parent_mulu=os.path.join(os.path.dirname(__file__),'data_mulu',self.data['name'])
                if os.path.isdir(parent_mulu):
                    pass
                else:
                    os.mkdir(parent_mulu)
                run_dir = os.path.join(parent_mulu, str(time.time()))
                self.data['run_dir']=run_dir
                try:
                    os.chdir(run_dir)
                except:
                    os.mkdir(run_dir)
                    os.chdir(run_dir)
                os.popen('git init')
                find_git={}
                for k, i in enumerate(self.data['git_path']):
                    # 查找git地址
                    zanshi_mulu = os.path.join(run_dir, i.split('/')[-1].split('.')[0] + self.data['git_branch'][k])
                    find_git[os.path.basename(i).split('.git')[0]+self.data['git_branch'][k]]=i
                    os.mkdir(zanshi_mulu)
                    open(os.path.join(zanshi_mulu, '__init__.py'), 'w').close()
                    os.chdir(zanshi_mulu)
                    os.popen('git init')
                    if 'http://' not in i:
                        i = 'http://' + i
                    #i = i.split('http://')[-1]
                    os.system('git clone  -b  %s    %s' % (self.data['git_branch'][k], i))
                self.data['run_id']=str(time.time())+str(random.randint(0,100))
                piliang_run(json.dumps(self.data),find_git)
                for parent, dirnames, filenames in os.walk(self.data['run_dir']):
                    for filename in filenames:
                        os.chmod(os.path.join(parent, filename), stat.S_IWRITE)

        # s删除多余文件夹
        for i in os.listdir(os.path.dirname(self.data['run_dir'])):
            if os.path.isdir(os.path.join(os.path.dirname(self.data['run_dir']), i)):
                try:
                    shutil.rmtree(os.path.join(os.path.dirname(self.data['run_dir']), i))
                except:
                    pass
        run_statu_change('over', self.data['id'], self.data['server_ip'])
        if 'dingshi' not in self.data['id']:
            run_statu_change('run', self.data['name'], self.data['server_ip'])
        time1=time.time()
        end_time=time1-time0
        run_statu_change('end_time',json.dumps({'end_time':end_time,'id':self.data['id']}), self.data['server_ip'])
        s = email_detail
        if s['receive'].strip() != '' and s['send'].strip() != '':
            send_emali(self.data['name'], self.data['id'].split('dingshi')[-1], email_detail,os.path.join(self.data['server_di'],'test/example.db'),self.data['server_ip'],self.data['statu'],self.data['pic_mulu'])
        '''
        result_path=os.path.join(r"C:\HGTP_server - test\app\templates\result",self.data[0]+'.html')
        now = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))  # 输出当前时间
        fp = open(result_path, 'wb')
        runner = HtmlTestRunner.HtmlTestRunner(stream=fp, title=u'用例执行情况', description=u'报告:')
        runner.run(unittest.defaultTestLoader.discover(os.path.join(r'E:\run_mulu',self.data[0]), pattern="*.py", top_level_dir=None))
        fp.close()
        db = sqlite3.connect(r'C:\HGTP_server - test\example.db')
        cu = db.cursor()
        time.sleep(1)
        cu.execute('update  run  set statu=0 where name="%s"' % self.data[0])
        db.commit()
        db.close()
        '''

def start():
    while 1:
        print(__name__)
        print('==========================')
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #定义socket类型，网络通信，TCP
        hostname = socket.gethostname()
        k=('127.0.0.1',8061)
        s.bind(k)
        s.listen(15)#开始TCP监听
        #接口实时调试数据池
        basedir = os.path.abspath(os.path.dirname(__file__))
        conn,addr=s.accept()   #接受TCP连接，并返回新的套接字与IP地址
        data=conn.recv(4096)   #把接收的数据实例化
        print(data)
        print('============================================')
        ub=MyThread(data)
        ub.start()