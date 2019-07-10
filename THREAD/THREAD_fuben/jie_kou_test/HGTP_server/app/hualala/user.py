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
import sqlite3
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import datetime
import shutil
def user(fun):
    def user_a():
        fun()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        if request.method == 'GET':
            user_detail = [list(i) for i in cu.execute('select * from user ').fetchall()]
            db.close()
            return render_template('/hualala/pages/user.html', user_detail= user_detail)
        elif request.method == 'POST':
            if request.form['statu']=='quanxian':
                name=cu.execute('select name from user where ip="%s" order by time desc limit 0,1'   %(request.remote_addr)).fetchall()[0][0]
                if name=='sun':
                  return jsonify(name='all')
                else:
                    return jsonify(name=name)
            if request.form['statu']=='add_use':
               name = request.form['name']
               ip=request.remote_addr
               user_check = [list(i)  for i in cu.execute('select name from user where name="%s" '%name).fetchall()]
               name=request.form['name']
               passs=request.form['pass']
               try:
                os.mkdir(os.path.join(current_app.config.get('ALLRUN_FILE'), name))
               except:
                   pass
               if name.strip()=='':
                   a=u'用户名不能为空'
               elif len(user_check)==0:
                   a='success'
                   cu.executemany('INSERT INTO user VALUES (?,?,?,?,?)',
                           [(name, passs,time.time(), '0','')])
                   db.commit()
               else:
                   a=u'用户名重复'
            elif request.form['statu']=='delete_use':
                name = request.form['name']
                try:
                   shutil.rmtree(os.path.join(current_app.config.get('RUN_FILE'), name))
                except:
                    pass
                cu.execute('delete from user where name=? ', (request.form['name'], ))
                cu.execute('delete from email_address where user=? ', (request.form['name'],))
                cu.execute('delete from run where name=? ', (request.form['name'],))
                cu.execute('delete from git_detail where submit=? ', (request.form['name'],))
                db.commit()
                a='delete-success'
            elif request.form['statu']=='change_password':
               name=request.form['name']
               password=request.form['password']
               cu.execute('update user set pass="%s" where name="%s" ' %(password,request.form['name'],))
               db.commit()
               a='change-success'
            db.close()
            return jsonify(a=a)
    return user_a

#serve 主页面

def server(fun):
    def server():
        fun()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        if request.method == 'GET':
            server_detail = [list(i) for i in cu.execute('select * from all_server ').fetchall()]
            xiancheng_detail=[i for i in cu.execute('select count(server) from dingshi_run  where statu="1"').fetchall()]
            for k,i  in enumerate(server_detail):
                server_detail[k].append(cu.execute('select count(*) from dingshi_run  where server="%s" and statu="1"'% i[1]).fetchall()[0][0])
            db.close()
            return render_template('/hualala/pages/server.html', user_detail= server_detail)
    return server
