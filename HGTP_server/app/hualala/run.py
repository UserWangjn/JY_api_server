# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\jieyuelianhe\old_all_server\HGTP_server\app\hualala\run.py
# Compiled at: 2019-02-20 15:28:42
__author__ = 'SUNZHEN519'
from tempfile import mktemp
from app import app
from flask import send_from_directory, send_file, Response
import socket, os, json, urllib2, re, chardet, time, shutil, sqlite3, smtplib
from email.mime.text import MIMEText
import urllib2
from tempfile import mktemp
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
import datetime, unittest, HTMLTestRunner, functools

def run_hualala(fun):

    def zzds():
        fun()
        if 'today_ci_pic' in current_app.config.keys():
            current_app.config.pop('today_ci_pic')
        if 'seven_ci_pic' in current_app.config.keys():
            current_app.config.pop('seven_ci_pic')
        if 'local_seven_pic' in current_app.config.keys():
            current_app.config.pop('local_seven_pic')
        job = request.form['job'].split('<span class="caret"></span>')[0]
        job = json.dumps({'name': job, 'result': ''})
        if 'job_id' in request.form.keys():
            job_id = request.form['job_id']
        else:
            job_id = ''
        job = json.dumps({'name': job, 'result': '', 'job_id': job_id})
        email_detail = json.dumps({'send': request.form['send_email_user'], 'receive': request.form['email'], 'title': request.form['emali_title']})
        git_path = [ i.strip() for i in request.form['all_path'].split('#') if i.strip() != '' ]
        git_branch = [ i.strip() for i in request.form['all_branch'].split('#') if i.strip() != '' ]
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        if request.form['run_server'] == u'自动分发' or request.form['run_server'] == 'Automatic distribution':
            if len(cu.execute('select server from dingshi_run  where statu="1"').fetchall()) == 0:
                run_server = cu.execute('select ip from all_server where statu="1" ').fetchall()[0][0]
            else:
                xiancheng_detail = [ i[0] for i in cu.execute('select server from dingshi_run  where statu="1"').fetchall() if i in [ z[0] for z in cu.execute('select ip from all_server where statu="1" ').fetchall() ] ]
                if len(xiancheng_detail) == 0:
                    run_server = cu.execute('select ip from all_server where statu="1" ').fetchall()[0][0]
                else:
                    all_server = [ i[0] for i in cu.execute('select ip from all_server where statu="1" ').fetchall() ]
                    server_num = {}
                    if len(all_server) != len(list(set(xiancheng_detail))):
                        for i in all_server:
                            if i not in xiancheng_detail:
                                run_server = i

                    else:
                        for k in xiancheng_detail:
                            server_num[k] = xiancheng_detail.count(k)

                        for z in server_num.keys():
                            if server_num[z] == min(server_num.values()):
                                run_server = z
                                break

        else:
            run_server = request.form['run_server']
        if 'statue' in request.form.keys() and request.form['statue'] == 'shishi':
            name = cu.execute('select name from user where ip="%s" order by time desc limit 0,1' % request.headers.get('X-Real-IP')).fetchall()[0][0]
            if len(cu.execute('select  statu from dingshi_run where name=? and run_time=?', (name, u'实时')).fetchall()) != 0 and cu.execute('select  statu from dingshi_run where name=? and run_time=?', (name, u'实时')).fetchall()[0][0] == '1':
                return jsonify(statu='running')
        if 'statue' in request.form.keys() and request.form['statue'] == 'jiekou_shishi':
            name = cu.execute('select name from user where ip="%s" order by time desc limit 0,1' % request.headers.get('X-Real-IP')).fetchall()[0][0]
            if len(cu.execute('select  statu from dingshi_run where name=? and run_time=?', (name, u'接口实时')).fetchall()) != 0 and cu.execute('select  statu from dingshi_run where name=? and run_time=?', (name, u'接口实时')).fetchall()[0][0] == '1':
                return jsonify(statu='running')
        try:
            name = request.form['name']
        except:
            name = cu.execute('select name from user where ip="%s" order by time desc limit 0,1' % request.headers.get('X-Real-IP')).fetchall()[0][0]
        if 'run_time' in request.form.keys():
            run_time = request.form['run_time']
        else:
            run_time = str(time.time())
        user_name = [ i.strip() for i in request.form['all_name'].split('#') if i.strip() != '' ]
        if request.form.has_key('statu') and 'dingshi' in request.form['statu'] and 'run_statu' in request.form.keys():
            if 'everyday' not in request.form['run_statu'].strip():
                run_time = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '  ' + run_time
            if request.form['statu'] == 'dingshi':
                all = cu.execute('select id from  dingshi_run where name="%s"  and statu in ("0","1","2")order by update_time asc' % name).fetchall()
            else:
                if request.form['statu'] == 'jiekou_dingshi':
                    all = cu.execute('select id from  dingshi_run where name="%s"  and statu in ("0","1","2")order by update_time asc' % name).fetchall()
                if len(all) > 4:
                    for i in all[-4:]:
                        cu.execute('delete from dingshi_run where id=%s ' % i)
                        strr = '#' + str(all[(-1)])
                        db.commit()

                try:
                    if 'everyday' in request.form['time'].encode('utf-8'):
                        z = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '  ' + request.form['time'].encode('utf-8').split('everyday')[(-1)].strip()
                        timeArray = time.strptime(z, '%Y-%m-%d %H:%M')
                    else:
                        timeArray = time.strptime(request.form['time'].encode('utf-8').split('：')[(-1)].strip(), '%Y-%m-%d %H:%M')
                    timestamp = time.mktime(timeArray)
                except:
                    return jsonify(statu='error')

            if request.form['statu'] == 'dingshi':
                cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)', [(name, time.time(), request.form['time'], request.form['all_path'], '0', email_detail, '', '{}', request.form['all_branch'], job, run_server)])
            else:
                if request.form['statu'] == 'jiekou_dingshi':
                    cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)', [
                     (name, time.time(),
                      request.form['time'],
                      request.form['all_path'], '0',
                      email_detail, '', '{}',
                      request.form['all_branch'], job,
                      run_server)])
            db.commit()
            html = '  <tr  class="dingshi_detail"    name="{{i[4]}}"><td   >{{i[1]}}</td><td>  {{i[2]}}</td><td>{{i[3]}}</td> </tr>'
            if request.form['statu'] == 'dingshi':
                dingshi_detail = [ [i[1], i[2], i[4], i[(-1)]] for i in cu.execute('select * from dingshi_run where name="%s" and statu in ("0","1","2") order by update_time desc ' % name).fetchall() ]
            else:
                if request.form['statu'] == 'jiekou_dingshi':
                    dingshi_detail = [ [i[1], i[2], i[4], i[(-1)]] for i in cu.execute('select * from dingshi_run where name="%s" and run_time like "%s" order by update_time desc ' % (name, u'接口%')).fetchall() ]
            db.close()
            for k, i in enumerate(dingshi_detail):
                i.insert(0, i[0])
                i[1] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(i[0])))
                if i[(-2)].strip() in ('0', '3'):
                    i[-2] = 'ready'
                elif i[(-2)].strip() in ('1', '4'):
                    i[-2] = 'running'
                elif i[(-2)].strip() in ('2', '5'):
                    i[-2] = 'over'

            s = ''
            for i in dingshi_detail:
                s += html.replace('{{i[4]}}', str(i[4])).replace('{{i[1]}}', i[1]).replace('{{i[2]}}', i[2]).replace('{{i[3]}}', i[3])

            return jsonify(statu='success', html=s)

        if len(cu.execute('select name from run where name="%s"' % name).fetchall()) == 0:
            cu.executemany('INSERT INTO  run values (?,?,?,?,?,?,?)', [(1, name, request.headers.get('X-Real-IP'), request.form['all_path'], time.time(), run_time, email_detail)])
            db.commit()
        else:
            cu.executemany('update  run  set statu=0,ip=?,mulu=?,time=?,time_run=? ,email=? where name=?', [(request.headers.get('X-Real-IP'), request.form['all_path'], time.time(), run_time, email_detail, name)])
            db.commit()
        if 'statu' not in request.form.keys():
            if request.form['statue'] == 'shishi':
                if len(cu.execute('select * from dingshi_run where name="%s"   and run_time="%s"' % (name, u'实时')).fetchall()) == 0:
                    cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)', [(name, time.time(), u'实时', request.form['all_path'], '0', email_detail, '', '{}', request.form['all_branch'], job, run_server)])
                    db.commit()
                else:
                    cu.executemany(u'update  dingshi_run  set statu=1,name=?,update_time=?,all_git=?,email=?,git_branch=?,run_result="{}" ,job=?,server=? where name=? and run_time="实时"', [(name, time.time(), request.form['all_path'], email_detail, request.form['all_branch'], job, run_server, name)])
                    db.commit()
            elif request.form['statue'] == 'jiekou_shishi':
                cu.execute(u'delete from dingshi_run where run_time="接口实时" and name=? ', (name,))
                db.commit()
                cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)', [
                 (name, time.time(),
                  u'接口实时',
                  request.form['all_path'],
                  '0', email_detail,
                  '', '{}',
                  request.form['all_branch'],
                  job, run_server)])
                db.commit()
        if 'statue' not in request.form.keys():
            run_dir = os.path.join(current_app.config.get('ALLRUN_FILE'), name, str(time.time()))
            try:
                os.chdir(run_dir)
            except:
                os.mkdir(run_dir)
                os.chdir(run_dir)
            os.popen('git init')
            for k, i in enumerate(git_path):
                zanshi_mulu = os.path.join(run_dir, i.split('/')[(-1)].split('.')[0] + git_branch[k])
                os.mkdir(zanshi_mulu)
                open(os.path.join(zanshi_mulu, '__init__.py'), 'w').close()
                os.chdir(zanshi_mulu)
                os.popen('git init')
                if 'http://' not in i:
                    i = 'http://' + i
                i = i.split('http://')[(-1)]
                print 'git clone  -b  %s    %s' % (git_branch[k], i)
                os.system('git clone  -b  %s    %s' % (git_branch[k], i))

            if 'statue' in request.form.keys() and request.form['statue'] != 'jiekou_shishi':
                open(os.path.join(run_dir, '__init__.py'), 'w').close()
                for fpathe, dirs, fs in os.walk(run_dir):
                    for f in dirs:
                        if '.git' != f.strip() and '.idea' != f.strip():
                            open(os.path.join(fpathe, f, '__init__.py'), 'w').close()

            try:
                os.chdir('C:\\\\')
            except:
                pass

        else:
            run_dir = os.path.join(current_app.config.get('ALLRUN_FILE'), name)
        s = {}
        s['name'] = name
        b = run_dir.split(os.sep)
        s['run_dir'] = run_dir
        if 'statue' in request.form.keys() and request.form['statue'] != 'jiekou_shishi':
            open(os.path.join(run_dir, '__init__.py'), 'w').close()
        if 'statu' in request.form.keys():
            if request.form['statu'] in ('dingshi', 'jiekou_dingshi'):
                s['id'] = request.form['id']
        else:
            if request.form['statue'] == 'dingshi':
                id = cu.execute('select id from dingshi_run where name="%s" and run_time="%s" ' % (name, u'实时')).fetchall()[0][0]
                s['id'] = str(id)
            else:
                if request.form['statue'] == 'jiekou_shishi':
                    id = cu.execute('select id from dingshi_run where name="%s" and run_time="%s" ' % (name, u'接口实时')).fetchall()[0][0]
                    s['id'] = str(id)
                else:
                    if request.form['statue'] == 'url_shishi':
                        id = cu.execute('select id from dingshi_run where name="%s" and run_time="%s" ' % (name, u'实时')).fetchall()[0][0]
                        s['id'] = str(id)
        if run_server.strip() != '':
            port = cu.execute('select duan_kou from all_server where ip="%s"' % run_server).fetchall()[0][0]
        db.close()
        if 'statu' in request.form.keys():
            s['statu'] = request.form['statu']
        else:
            if 'statue' in request.form.keys():
                s['statu'] = request.form['statue']
        s['server_di'] = current_app.config.get('SERVER_DI')
        s['job_id'] = job_id
        if 'statue' not in request.form.keys():
            s['run_dir'] = os.path.join(s['server_di'], s['run_dir'].split(os.sep)[(-3)], s['run_dir'].split(os.sep)[(-2)], s['run_dir'].split(os.sep)[(-1)])
        hostname = socket.gethostname()
        s['server_ip'] = socket.gethostbyname(hostname)
        s['git_path'] = git_path
        if 'statue' in request.form.keys() and request.form['statue'] == 'url_shishi':
            s['statue'] = request.form['statue']
        s['git_branch'] = git_branch
        s['email_detail'] = email_detail
        s['job'] = job
        s['pic_mulu'] = current_app.config.get('RESULT_PICT_SAVE')
        data = json.dumps(s)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if run_server.strip() == '':
            port = cu.execute('select duan_kou from all_server where ip="%s"' % '172.16.32.141').fetchall()[0][0]
            s.connect(('192.168.151.224', port))
        else:
            s.connect((run_server, int(port)))
        data = data.replace('//', '')
        s.send(data)
        s.close()
        return jsonify(statu='scuess')

    return zzds


def run_result(path):
    loader = unittest.TestLoader()
    suite1 = unittest.defaultTestLoader.discover(path, pattern='*.py', top_level_dir='E:\\run_mulu\\lakala')
    now = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
    fp = open('D:\\python text\\11.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'用例执行情况', description=u'报告:')
    runner.run(suite1)
    fp.close()


def run_charge(fun):

    def charge():
        fun()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        try:
            name = cu.execute('select name from user where ip="%s" order  by time desc limit 0,1 ' % request.headers.get('X-Real-IP')).fetchall()[0][0]
        except:
            return jsonify(statu='0')

        statu = cu.execute('select statu from run where name="%s" ' % name).fetchall()[0][0]
        return jsonify(statu=statu)

    return charge


def add_file_detail(func):

    @functools.wraps(func)
    def aa():
        func()
        if request.method == 'POST':
            if request.form['type'] == 'jiekou':
                db = sqlite3.connect(current_app.config.get('JIE_KOU'))
            else:
                db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
            cu = db.cursor()
            cu.execute('update git_detail set detail="%s" where name="%s"  and  submit="%s" ' % (request.form['detail'], request.form['git'], request.form['name']))
            db.commit()
            db.close()
            return jsonify(a='1')
        if request.method == 'GET':
            if request.args.get('type') == 'jiekou':
                db = sqlite3.connect(current_app.config.get('JIE_KOU'))
            else:
                db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
            cu = db.cursor()
            detail = cu.execute('select detail from  git_detail  where name="%s"  and  submit="%s" ' % (request.args.get('git'), request.args.get('name'))).fetchall()[0][0]
            db.commit()
            db.close()
            return jsonify(a=detail)

    return aa


def dingshi_result(func):

    def aaaa():
        func()
        if request.method == 'POST':
            if request.form['type'] == 'jiekou':
                db = sqlite3.connect(current_app.config.get('JIE_KOU'))
            else:
                db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
            cu = db.cursor()
            name = cu.execute('select name from user where ip="%s" order  by time desc limit 0,1 ' % request.headers.get('X-Real-IP')).fetchall()[0][0]
            db.close()
            id = request.form['update_time']
            url = os.path.join(current_app.config.get('RUN_FILE'), name)
            file_name = '#' + str(id)
            session['id'] = id
            for parent, dirnames, filenames in os.walk(url):
                for filename in filenames:
                    if file_name in filename:
                        path = os.path.join(parent, filename)
                        print path

            db.close()
            session[name] = path
            return jsonify(statu='success')
        if request.args.get('type') == 'jiekou':
            db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        else:
            db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        z = cu.execute('select run_result from dingshi_run where id=?', (session['id'],)).fetchall()[0][0]
        z = json.loads(z)
        db.close()
        print session[name].replace('\\', '/')
        return render_template('/hualala/pages/test_result.html', time=str(time.time()), z=z)

    return aaaa


def open_dingshi_detail(func):

    def open_dingshi_det():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        name = cu.execute('select name from user where ip="%s" order  by time desc limit 0,1 ' % request.headers.get('X-Real-IP')).fetchall()[0][0]
        html = '  <tr  class="dingshi_detail"    name="{{i[4]}}"><td   >{{i[1]}}</td><td>  {{i[2]}}</td><td>{{i[3]}}</td><td>erere</td></tr>'
        if 'statu' in request.form.keys() and request.form['statu'] == 'jiekou_dingshi':
            dingshi_detail = [ [i[1], i[2], i[4], i[6]] for i in cu.execute('select * from dingshi_run where name="%s" and run_time like "%s" order by update_time desc ' % (name, u'接口%')).fetchall() ]
            server_di = [ i[0] for i in cu.execute('select server from dingshi_run where name="%s"    and run_time like "%s"  order by update_time desc ' % (name, u'接口%')).fetchall()
                        ]
        else:
            dingshi_detail = [ [i[1], i[2], i[4], i[6]] for i in cu.execute('select * from dingshi_run where name="%s" and statu in ("0","1","2") order by update_time desc ' % name).fetchall() ]
            server_di = [ i[0] for i in cu.execute('select server from dingshi_run where name="%s"    and statu in ("0","1","2")  order by update_time desc ' % name).fetchall()
                        ]
        db.close()
        for k, i in enumerate(dingshi_detail):
            i.insert(0, i[0])
            i[1] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(i[0])))
            if i[(-2)].strip() in ('0', '3'):
                i[-2] = 'ready'
            else:
                if i[(-2)].strip() in ('1', '4'):
                    i[-2] = 'running'
                else:
                    if i[(-2)].strip() in ('2', '5'):
                        i[-2] = 'over'
            i.append(server_di[k])

        s = ''
        for i in dingshi_detail:
            s += html.replace('{{i[4]}}', str(i[4])).replace('{{i[1]}}', i[1]).replace('{{i[2]}}', i[2]).replace('{{i[3]}}', i[3]).replace('erere', i[5])

        return jsonify(statu='success', html=s)

    return open_dingshi_det


def change_run_statu(func):

    def ceshizhon111ag():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        data = 'success'
        if request.form['statu'] == 'running':
            if 'dingshi' in request.form['data']:
                cu.execute('update  dingshi_run  set statu=1 where id=%s ' % int(request.form['data'].split('dingshi')[(-1)]))
            else:
                cu.execute('update  dingshi_run  set statu=1 where id=%s ' % int(request.form['data']))
        else:
            if request.form['statu'] == 'over':
                if 'dingshi' in request.form['data']:
                    cu.execute('update  dingshi_run  set statu=2 where id=%s ' % int(request.form['data'].split('dingshi')[(-1)]))
                else:
                    cu.execute('update  dingshi_run  set statu=2 where id=%s ' % int(request.form['data']))
            else:
                if request.form['statu'] == 'run':
                    cu.execute('update  run  set statu=0 where name="%s" ' % request.form['data'])
                else:
                    if 'job_result' in request.form['statu']:
                        data = json.loads(request.form['data'])
                        job_detail = json.loads(cu.execute('select job from dingshi_run where id=?', (data['id'],)).fetchall()[0][0])
                        job_detail['result'] = data['result']['result']
                        cu.execute('update  dingshi_run  set job=? where id=? ', (json.dumps(job_detail), data['id']))
                    else:
                        if request.form['statu'] == 'jekins':
                            data = json.loads(request.form['data'])
                            id = data['job_id']
                            data = cu.execute('select * from   jekins  where id=?', (id,)).fetchall()[0]
                        else:
                            if request.form['statu'] == 'end_time':
                                use_data = json.loads(request.form['data'])
                                id = use_data['id']
                                end_time = use_data['end_time']
                                data = json.loads(cu.execute('select job from dingshi_run where id=?', (id,)).fetchall()[0][0])
                                data['end_time'] = end_time
                                cu.execute('update  dingshi_run  set job=? where id=? ', (
                                 json.dumps(data), int(id)))
                            else:
                                if request.form['statu'] == 'email':
                                    data = json.loads(request.form['data'])
                                    data = cu.execute('select * from fajianren where name="%s" and email_user="%s"' % (data['name'], data['send_email'])).fetchall()[0]
        db.commit()
        db.close()
        return jsonify(data=data)

    return ceshizhon111ag


def update_host(func):

    def ceshizonga():
        if request.method == 'post':
            func()
            return jsonify(statu='success')

    return ceshizonga