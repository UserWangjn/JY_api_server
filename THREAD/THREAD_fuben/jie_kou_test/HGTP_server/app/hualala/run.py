# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
# -*- coding: utf-8 -*-
from tempfile import mktemp
from app import app
from flask import send_from_directory,send_file,Response
import socket
import paramiko
import os
import json
import urllib2
import re
import  chardet
import time
import shutil
import sqlite3
import smtplib
from email.mime.text import MIMEText
import urllib2
from tempfile import mktemp
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import datetime
import unittest
import HTMLTestRunner
import functools
def run_hualala(fun):
    @functools.wraps(fun)
    def zz():
        fun()
        job=request.form['job'].split('<span class="caret"></span>')[0]
        job=json.dumps({'name':job,'result':''})
        email_detail=json.dumps({'send':request.form['send_email_user'],'receive':request.form['email'],'title':request.form['emali_title']})
        #获取文件目录列表
        git_path = [i.strip() for i in request.form['all_path'].split('#') if i.strip() != '']
        git_branch=[i.strip() for i in request.form['all_branch'].split('#') if i.strip() != '']
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        #自动分发
        if request.form['run_server']==u'自动分发':
          if len(cu.execute('select server from dingshi_run  where statu="1" or statu="4"').fetchall())==0:
              run_server = cu.execute('select ip from all_server where statu="1" ').fetchall()[0][0]
          else:
            xiancheng_detail= [i[0] for i in cu.execute('select server from dingshi_run  where statu="1"  or statu="3"').fetchall()]
            if len(xiancheng_detail)==0:
                run_server=cu.execute('select ip from all_server where statu="1" ').fetchall()[0][0]
            else:
              all_server = [i[0] for i in cu.execute('select ip from all_server where statu="1" ').fetchall()]
              server_num = {}
              if len(all_server)!=len(list(set(xiancheng_detail))) :
                for i in all_server:
                  if i not in xiancheng_detail   :
                      run_server=i

              else:
                      for k in xiancheng_detail:
                          server_num[k]=xiancheng_detail.count(k)
                      for z in server_num.keys():
                          if server_num[z]==min(server_num.values()):
                              run_server=z
                              break
        else:
            run_server=request.form['run_server']

        if 'statue' in request.form.keys()  and request.form['statue']=='shishi':
            name = cu.execute(
                'select name from user where ip="%s" order by time desc limit 0,1' % (request.remote_addr)).fetchall()[
                0][0]
            if request.form['type']=='url' and  len(cu.execute('select  statu from dingshi_run where name=? and run_time=? and statu="1"',(name,u'实时' ) ).fetchall())!=0 :
                return jsonify(statu='running')
            if request.form['type']=='jie_kou' and  len(cu.execute('select  statu from dingshi_run where name=? and run_time=? and statu="4"',(name,u'实时' ) ).fetchall())!=0 :
                return jsonify(statu='running')
        try:
           name=request.form['name']
        except:
            name = cu.execute(
                'select name from user where ip="%s" order by time desc limit 0,1' % (request.remote_addr)).fetchall()[
                0][0]
        #请求时间,如果有传递过来run_time则使用传递过来的，如果没有则用当前时间戳
        if 'run_time'  in request.form.keys():
            run_time=request.form['run_time']
        else:
          run_time = str(time.time())
        user_name = [i.strip() for i in request.form['all_name'].split('#') if i.strip() != '']
             #os.popen('git pull http://sunzhen:6551268Sun@' + str(user_name[k]))
        #根据目录copy相应文件到设置的run文件夹下,之前删除以用户名明明的文件夹，
        if request.form.has_key('statu') and request.form['statu']=='dingshi'and 'run_statu'  in request.form.keys():
            if 'everyday' not   in request.form['run_statu'].strip():
                 run_time=time.strftime('%Y-%m-%d',time.localtime(time.time())) +'  '+run_time
            if request.form['type']=='url':
               all=cu.execute('select * from  dingshi_run where name="%s" and statu in (0,1,2) order by update_time asc'  % (name ) ).fetchall()
            else:
                all = cu.execute(
                    'select * from  dingshi_run where name="%s" and statu in (3,4,5) order by update_time asc' % (
                    name)).fetchall()

            if len(all)>4:
                 if request.form['type'] == 'url':
                      limit_detail=cu.execute('select id from  dingshi_run where name="%s" and statu in (0,1,2)  order by update_time asc limit 0,1' % (name)).fetchall()[0][0]
                 else:
                     limit_detail = cu.execute(
                         'select id from  dingshi_run where name="%s" and statu in (3,4,5)  order by update_time asc limit 0,1' % (
                         name)).fetchall()[0][0]
                 cu.execute('delete from dingshi_run where id=%s '  % (limit_detail) )
                 strr='#'+str(limit_detail)
                 db.commit()
            try:
                if 'everyday' in request.form['time'].encode('utf-8'):
                    z=time.strftime('%Y-%m-%d', time.localtime(time.time()))+'  '+request.form['time'].encode('utf-8').split('everyday')[-1].strip()
                    timeArray = time.strptime(z,"%Y-%m-%d %H:%M")
                else:
                  timeArray = time.strptime(request.form['time'].encode('utf-8').split('：')[-1].strip(), "%Y-%m-%d %H:%M")
                timestamp = time.mktime(timeArray)
            except:
                return jsonify(statu='error')
            if request.form['type'] == 'url':
              cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)',[( name,time.time(),request.form['time'],request.form['all_path'],'0',email_detail,'','{}',request.form['all_branch'],job,run_server)])
            else:
                cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)', [(name, time.time(),
                                                                                                 request.form['time'],
                                                                                                 request.form[
                                                                                                     'all_path'], '3',
                                                                                                 email_detail, '', '{}',
                                                                                                 request.form[
                                                                                                     'all_branch'], job,
                                                                                                 run_server)])

            db.commit()
            html='  <tr  class="dingshi_detail"    name="{{i[4]}}"><td   >{{i[1]}}</td><td>  {{i[2]}}</td><td>{{i[3]}}</td> </tr>'
            if request.form['type'] == 'url':
              dingshi_detail = [[i[1], i[2], i[4],i[-1]] for i in cu.execute(
                'select * from dingshi_run where name="%s" and statu in (0,1,2)order by update_time desc ' % (name)).fetchall()]
            else:
                dingshi_detail = [[i[1], i[2], i[4], i[-1]] for i in cu.execute(
                    'select * from dingshi_run where name="%s" and statu in (3,4,5) order by update_time desc ' % (name)).fetchall()]
            db.close()
            for k, i in enumerate(dingshi_detail):
                i.insert(0, i[0])
                i[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i[0])))
                if i[-2].strip() == '0':
                    i[-2] = u'ready'
                elif i[-2].strip() == '1':
                    i[-2] = u'running'
                elif i[-2].strip() == '2':
                    i[-2] = u'over'
            s=''
            for i in dingshi_detail:
                s+=html.replace('{{i[4]}}',str(i[4])).replace('{{i[1]}}',i[1]).replace('{{i[2]}}',i[2]).replace('{{i[3]}}',i[3])
            return jsonify(statu="success",html=s)
        if  len(cu.execute('select name from run where name="%s"' % name).fetchall())==0:
            cu.executemany('INSERT INTO  run values (?,?,?,?,?,?,?)',[(1, name,request.remote_addr,request.form['all_path'],time.time(), run_time,email_detail)])
            db.commit()
        else:
            cu.executemany('update  run  set statu=0,ip=?,mulu=?,time=?,time_run=? ,email=? where name=?', [(request.remote_addr,request.form['all_path'],time.time(), run_time, email_detail,name)])
            db.commit()
        if 'statu' not in request.form.keys():
            if request.form['type']=='url':
                      if   len(cu.execute('select * from dingshi_run where name="%s" and stau in (0,1,2) and run_time="%s"' % (name,u'实时')).fetchall())==0:
                        cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)',[( name,time.time(),u'实时',request.form['all_path'],'0',email_detail,'','{}',request.form['all_branch'],job,run_server)])
                        db.commit()
                      else:
                        cu.executemany('update  dingshi_run  set statu=1,name=?,update_time=?,all_git=?,email=?,git_branch=?,run_result="{}" ,job=?,server=? where name=? and run_time="实时"', [(name,time.time(),request.form['all_path'],email_detail,request.form['all_branch'],job,run_server,name)])
                        db.commit()
            else:
                if len(cu.execute('select * from dingshi_run where name="%s" and stau in (3,4,5) and run_time="%s"' % (name, u'实时')).fetchall()) == 0:
                    cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)', [(name, time.time(),
                                                                                                     u'实时',
                                                                                                     request.form[
                                                                                                         'all_path'],
                                                                                                     '3', email_detail,
                                                                                                     '', '{}',
                                                                                                     request.form[
                                                                                                         'all_branch'],
                                                                                                     job, run_server)])
                    db.commit()
                else:
                    cu.executemany(
                        'update  dingshi_run  set statu=4,name=?,update_time=?,all_git=?,email=?,git_branch=?,run_result="{}" ,job=?,server=? where name=? and run_time="实时"',
                        [(name, time.time(), request.form['all_path'], email_detail, request.form['all_branch'], job,
                          run_server, name)])
                    db.commit()
        #拉下来git代码
        #if 'run_time'  in request.form.keys():
           #run_dir=os.path.join(current_app.config.get('ALLRUN_FILE'),name,str(time.time()))
        run_dir = os.path.join(current_app.config.get('ALLRUN_FILE'), name, str(time.time()))
        try:
            os.chdir(run_dir)
        except:
            os.mkdir(run_dir)
            os.chdir(run_dir)
        os.popen('git init')
        for k,i in enumerate(git_path):
            #查找git地址
               zanshi_mulu=os.path.join(run_dir,i.split('/')[-1].split('.')[0]+git_branch[k])
               os.mkdir(zanshi_mulu)
               open(os.path.join(zanshi_mulu,'__init__.py'),'w').close()
               os.chdir(zanshi_mulu)
               os.popen('git clone  -b  %s http://sunzhen:6551268Sun@%s' %( git_branch[k],i))
        #在每个目录下面增加构造文件
        open(os.path.join(run_dir, '__init__.py'), 'w').close()
        for fpathe, dirs, fs in os.walk(run_dir):
            for f in dirs:
                if '.git'!=f.strip() and '.idea'!=f.strip():
                  open(os.path.join(fpathe, f, '__init__.py'), 'w').close()
        os.chdir(r'C:')
        s={}
        s['name']=name
        b = run_dir.split(os.sep)
        s['run_dir']=run_dir
        open(os.path.join(run_dir, '__init__.py'), 'w').close()
        if 'statu' in request.form.keys()  and request.form['statu']=='dingshi':
            s['id']=request.form['id']
        else:
            if request.form['type']=='url':
                    id=cu.execute(
                    'select id from dingshi_run where name="%s" and run_time="%s" and statu in (0,1,2) ' % (name,u'实时')).fetchall()[0][0]
                    s['id']=str(id)
            else:
                id = cu.execute(
                    'select id from dingshi_run where name="%s" and run_time="%s" and statu in (3,4,5) ' % (
                    name, u'实时')).fetchall()[0][0]
                s['id'] = str(id)

        if run_server.strip()!='':
            port=cu.execute('select duan_kou from all_server where ip="%s"' % (run_server)).fetchall()[0][0]
        db.close()
        #获取ip地址
        s['server_di']=r'\\172.16.32.103\all_new'
        #将本地目录转化为网络目录
        s['run_dir']=os.path.join(s['server_di'],s['run_dir'].split(os.sep)[-3],s['run_dir'].split(os.sep)[-2],s['run_dir'].split(os.sep)[-1])
        hostname = socket.gethostname()
        s['server_ip'] = socket.gethostbyname(hostname)
        data = json.dumps(s)
        #socket lian jie
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if run_server.strip()=='':
               s.connect(("172.16.32.103", 8059))
        else:
            s.connect((run_server, int(port)))
        #s.connect(("192.168.4.72", 8059))
        s.send(data)
        s.close()
        return jsonify(statu='scuess')
    return zz
#根据目录运行脚本病返回结果 html
def run_result(path):
    loader = unittest.TestLoader()
    # case_dir = [r'C:\11\HGTP', r'C:\11\2']
    suite1 = unittest.defaultTestLoader.discover(path, pattern="*.py", top_level_dir=r'E:\run_mulu\lakala')
    # suite2 = unittest.TestSuite(unittest.defaultTestLoader.discover(r'C:\22', pattern="test*.py", top_level_dir=None))
    now = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))  # 输出当前时间
    fp = open(r"D:\python text\11.html", 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'用例执行情况', description=u'报告:')
    runner.run(suite1)
    fp.close()
#运行状态检查
def run_charge(fun):
    def charge():
        fun()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        try:
          name = cu.execute(
            'select name from user where ip="%s" order  by time desc limit 0,1 ' % request.remote_addr).fetchall()[0][0]
        except:
            return jsonify(statu='0')
        statu = cu.execute('select statu from run where name="%s" ' % name).fetchall()[0][0]
        #判断状态如果状态为0，说明已经运行完毕，则发送邮件
        return jsonify(statu=statu)
    return charge


#增加git库备注详细信息
def add_file_detail(func):
    @functools.wraps(func)
    def aa():
      func()
      if request.method=='POST':
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        cu.execute('update git_detail set detail="%s" where name="%s"  and  submit="%s" ' %(request.form['detail'],request.form['git'],request.form['name']))
        db.commit()
        db.close()
        return jsonify(a='1')
      if request.method == 'GET':
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        detail=cu.execute('select detail from  git_detail  where name="%s"  and  submit="%s" ' %(request.args.get('git'),request.args.get('name'))).fetchall()[0][0]
        db.commit()
        db.close()
        return jsonify(a=detail)
    return aa



#查看定时运行的结果文件
def dingshi_result(func):
    def aaaa():
      func()
      db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
      cu = db.cursor()
      name = cu.execute(
          'select name from user where ip="%s" order  by time desc limit 0,1 ' % request.remote_addr).fetchall()[0][0]
      db.close()
      if request.method=='POST':
        id=request.form['update_time']
        url = os.path.join(current_app.config.get('RUN_FILE'), name)
        file_name='#'+str(id)
        session['id']=id
        for parent, dirnames, filenames in os.walk(url):
            for filename in filenames:
                if file_name in filename  :
                    path=os.path.join(parent, filename)
                    print path
        db.close()
        session[name]=path
        return jsonify(statu='success')
      else:
          db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
          cu = db.cursor()
          z = cu.execute('select run_result from dingshi_run where id=?',(session['id'], )).fetchall()[0][0]
          z=json.loads(z)
          db.close()
          print session[name].replace("\\", '/')
          return render_template('/hualala/pages/test_result.html',time=str(time.time()),z= z)
    return aaaa



#打开定时运行详细页面
def open_dingshi_detail(func):
    def open_dingshi_det():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        name = cu.execute(
            'select name from user where ip="%s" order  by time desc limit 0,1 ' % request.remote_addr).fetchall()[0][0]
        html = '  <tr  class="dingshi_detail"    name="{{i[4]}}"><td   >{{i[1]}}</td><td>  {{i[2]}}</td><td>{{i[3]}}</td><td>erere</td></tr>'
        dingshi_detail = [[i[1], i[2], i[4], i[6]] for i in cu.execute(
            'select * from dingshi_run where name="%s" order by update_time desc ' % (name)).fetchall()]
        server_di=[i[0] for i in cu.execute(
            'select server from dingshi_run where name="%s" order by update_time desc ' % (name)).fetchall()]
        db.close()
        for k, i in enumerate(dingshi_detail):
            i.insert(0, i[0])
            i[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i[0])))
            if i[-2].strip() ==u'0':
                i[-2] = u'ready'
            elif i[-2].strip() == u'1':
                i[-2] = u'running'
            elif i[-2].strip() == u'2':
                i[-2] = u'over'
            i.append(server_di[k])
        s = ''
        for i in dingshi_detail:
            s += html.replace('{{i[4]}}', str(i[4])).replace('{{i[1]}}', i[1]).replace('{{i[2]}}', i[2]).replace(
                '{{i[3]}}', i[3]).replace('erere',i[5])
        return jsonify(statu="success", html=s)
    return open_dingshi_det





