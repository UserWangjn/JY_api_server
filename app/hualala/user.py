# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\jieyuelianhe\old_all_server\HGTP_server\app\hualala\user.py
# Compiled at: 2018-11-08 11:24:40
__author__ = 'SUNZHEN519'
from tempfile import mktemp
from app import app
from flask import send_from_directory, send_file, Response
import socket, os, json, urllib.request, urllib.error, urllib.parse, re, chardet, time, sqlite3
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
import datetime, shutil

def user(fun):

    def user_a():
        fun()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        if request.method == 'GET':
            user_detail = [ list(i) for i in cu.execute('select user.name,user.pass,user.time,user.statu,user.ip,user_team.team from user LEFT  OUTER JOIN user_team  on user.name=user_team.user ').fetchall() ]
            team_user = [ i[0] for i in cu.execute('select team from team ').fetchall() ]
            db.close()
            return render_template('/hualala/pages/user.html', user_detail=user_detail, team_user=team_user)
        if request.method == 'POST':
            if request.form['statu'] == 'quanxian':
                name = cu.execute('select name from user where ip="%s" order by time desc limit 0,1' % request.headers.get('X-Real-IP')).fetchall()[0][0]
                if name == 'sun':
                    return jsonify(name='all')
                return jsonify(name=name)
            if request.form['statu'] == 'add_use':
                name = request.form['name']
                ip = request.headers.get('X-Real-IP')
                user_check = [ list(i) for i in cu.execute('select name from user where name="%s" ' % name).fetchall() ]
                name = request.form['name']
                passs = request.form['pass']
                try:
                    os.mkdir(os.path.join(current_app.config.get('ALLRUN_FILE'), name))
                except:
                    pass

                if name.strip() == '':
                    a = '用户名不能为空'
                elif len(user_check) == 0:
                    a = 'success'
                    cu.executemany('INSERT INTO user VALUES (?,?,?,?,?)', [
                     (
                      name, passs, time.time(), '0', '')])
                    db.commit()
                else:
                    a = '用户名重复'
            else:
                if request.form['statu'] == 'delete_use':
                    name = request.form['name']
                    try:
                        shutil.rmtree(os.path.join(current_app.config.get('RUN_FILE'), name))
                    except:
                        pass

                    cu.execute('delete from user where name=? ', (request.form['name'],))
                    cu.execute('delete from email_address where user=? ', (request.form['name'],))
                    cu.execute('delete from run where name=? ', (request.form['name'],))
                    cu.execute('delete from git_detail where submit=? ', (request.form['name'],))
                    db.commit()
                    a = 'delete-success'
                else:
                    if request.form['statu'] == 'change_password':
                        name = request.form['name']
                        password = request.form['password']
                        cu.execute('update user set pass="%s" where name="%s" ' % (password, request.form['name']))
                        db.commit()
                        a = 'change-success'
            db.close()
            return jsonify(a=a)

    return user_a


def server(fun):

    def server():
        fun()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        if request.method == 'GET':
            server_detail = [ list(i) for i in cu.execute('select * from all_server ').fetchall() ]
            xiancheng_detail = [ i for i in cu.execute('select count(server) from dingshi_run  where statu="1"').fetchall() ]
            for k, i in enumerate(server_detail):
                server_detail[k].append(cu.execute('select count(*) from dingshi_run  where server="%s" and statu="1"' % i[1]).fetchall()[0][0])

            db.close()
            return render_template('/hualala/pages/server.html', user_detail=server_detail)

    return server


def add_user_team(fun):

    def add_user_team():
        fun()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        team_name = request.form['data']
        if len(cu.execute('select * from team where team="%s" ' % team_name).fetchall()) != 0:
            return jsonify(statu='重复')
        cu.executemany('INSERT INTO team VALUES (null,?)', [
         (
          team_name,)])
        db.commit()
        db.close()
        return jsonify(statu='success')

    return add_user_team


def gengxin_team(fun):

    def gengxin_team():
        fun()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        team_name = request.form['team_name']
        name = request.form['name']
        cu.execute('update local_tongji set user_team=? where name=?', (team_name, name))
        if len(cu.execute('select * from user_team where user="%s" ' % name).fetchall()) != 0:
            cu.execute('update user_team set team="%s" where user="%s" ' % (team_name, name))
        else:
            cu.executemany('INSERT INTO user_team VALUES (null,?,?)', [
             (
              name, team_name)])
        db.commit()
        db.close()
        return jsonify(statu='success')

    return gengxin_team