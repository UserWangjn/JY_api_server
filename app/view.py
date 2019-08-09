# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
# [GCC 8.2.1 20181127]
# Embedded file name: C:\jieyuelianhe\old_all_server\HGTP_server\app\view.py
# Compiled at: 2019-06-21 16:27:00
from tempfile import mktemp
from flask import send_from_directory, send_file, Response
import socket
from io import StringIO
from io import BytesIO
import os, sys
from .hualala.check_login import *
from .hualala.git_submit import *
import json, urllib.request, urllib.error, urllib.parse, re, chardet
from .jie_kou import *
from functools import wraps
from .zhixing import *
from .data_verification import *
from .yuansudingwei import *
import time, sqlite3
from .shell_name import *
from .form import *
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
import datetime, json
from io import StringIO
from io import BytesIO
from flask import make_response
bootstrap = Bootstrap(app)
UPLOAD_FOLDER = 'static/Uploads'

@app.before_request
def before_request():
    if 'path' in list(request.form.keys()) and request.form['path'] == 'server':
        pass
    else:
        statu = 0
        g.db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        g.cu = g.db.cursor()
        pubulic_url = ['upload_file', '/testtesttest', '/git_bianji', '/get_renwu_detail', '/debugging', '/chongou_test', '/login', '/get_sumint_statu', '/get_file_git', 'piliang_run_git_over', 'jiekou_result', 'add_jekins', 'ceshialert', 'change_run_statu', 'login', 'run_hualala', 'dingshi_result', 'change_run_statu', 'tongji_mail']
        for i in pubulic_url:
            if i in request.url:
                statu = 1

        if 'open_window_page_result' in request.url:
            statu = 1
        if statu == 1:
            session['deng_lu'] = True
            g.db.close()
        else:
            if 'deng_lu' not in list(session.keys()) or session['deng_lu'] != True:
                user = [ i[0] for i in g.cu.execute('select ip from user').fetchall() ]
                g.db.close()
                if request.headers.get('X-Real-IP') not in user and 'static' not in request.url:
                    return redirect(url_for('login_new'))
            else:
                g.db.close()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


from .lenove_jie_kou.wirte_logs import *

@app.route('/wirte_logs', methods=['POST', 'GET'])
def wirte_logs():
    pass


@app.route('/post', methods=['POST'])
def demo_post():
    return jsonify(a=request.form)


@app.route('/get', methods=['get'])
def demo_get():
    return jsonify(a=request.argv)


@app.route('/read_logs', methods=['POST', 'GET'])
def read_logs():
    ip = '127.0.0.1'
    return jsonify(a=2, b=3)
    if request.method == 'POST':
        linux = g.cu.execute('select linux from jie_kou_test where name="%s" and ip="%s"' % (request.form['name'], ip)).fetchall()[0][0]
        linux = eval(linux)
        hostname = linux['ip']
        username = linux['name']
        password = linux['password']
        if linux['string'].strip() == 'time':
            linux['string'] = datetime.datetime.now().strftime('%Y-%m-%d')
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname, 22, username, password, timeout=5)
        stdin, stdout, stderr = s.exec_command('tail -n  50 ' + linux['mu_lu'])
        k = str(linux['string']) + str(linux['string']).join(stdout.read().strip().split(linux['string'])[int('-' + linux['num']):])
        g.cu.execute('UPDATE jie_kou_test SET log=?,time=? WHERE num=? and name=? and ip=?', (
         k.decode('utf-8'), time.time(), 'run', request.form['name'], ip))
        g.db.commit()
        return jsonify(data=k)
    if request.method == 'GET':
        if request.args.get('shi') == 'yunxing_log':
            data = g.cu.execute('select log from jie_kou_test where name="%s" and ip="%s" and num="run"' % (
             request.args.get('name'), ip)).fetchall()[0]
            return jsonify(data=data)
        if request.args.get('shi') == 'bug_log':
            data = g.cu.execute('select log from jie_kou_test where name="%s" and ip="%s" and num="bug"' % (
             request.args.get('name'), ip)).fetchall()[0]
            return jsonify(data=data)
        if request.args.get('shi') == 'tiaoshi_log':
            data = g.cu.execute('select log from jie_kou_test where name="%s" and ip="%s" and num="debug"' % (
             request.args.get('name'), ip)).fetchall()[0]
            return jsonify(data=data)


@app.route('/linux_config', methods=['POST'])
def linux_config():
    if request.method == 'POST':
        linux = request.form['linux']
        config = request.form['config']
        name = request.form['name']
        if g.cu.execute('select * from jie_kou_test where name="%s"' % name).fetchall() == []:
            g.cu.executemany('INSERT INTO jie_kou_test VALUES (?,?,?,?,?,?,?,?)', [
             (
              'run', name, linux, 'no data', config, str(request.headers.get('X-Real-IP')), 'no data', time.time())])
            g.db.commit()
        else:
            g.cu.execute('UPDATE jie_kou_test SET name=?,linux=?,ifconfig=?,time=? WHERE num=? and name=? and ip=?', (
             name, linux, config, time.time(), 'run', name, request.headers.get('X-Real-IP')))
            g.db.commit()
        return jsonify(da=1)


@app.route('/jie_run', methods=['GET', 'POST'])
def jie_run():
    if request.method == 'GET':
        return render_template('/simple_page/yun_jiekou.html', data='11')
    if request.method == 'POST':
        jie_kou_test = request.form['shi']
        jie_name = request.form['name']
        data = g.cu.execute('select ifconfig from jie_kou_test where name="%s" and ip="%s"' % (jie_name, str(request.headers.get('X-Real-IP')))).fetchall()[0][0].split('\n')
        pon = kaifa_run(jie_kou_test, data)
        return jsonify(a=pon.x)


@app.route('/no_use', methods=['GET', 'POST'])
def jie_rueen():
    return render_template('/simple_page/yun_jiekou.html')


@app.route('/tabs_kaifa', methods=['GET', 'POST'])
def tabs_kaifa():
    if 'barcode' not in list(session.keys()) or session['barcode'].strip() == '':
        session['barcode'] = '201701221000005'
        table = ['no data', 'no data', 'no data']
        data = ['no data', 'no data', 'no data', 'no data', 'no data']
        return render_template('/simple_page/tabs_kaifa.html', b=table, value=data, b1=table, value1=data, b2=table, value2=data)
    conn_old = MySQLdb.connect(host='10.199.128.61', port=3309, user='vis', passwd='vispvip', db='visAdmin', cursorclass=MySQLdb.cursors.DictCursor, charset='utf8')
    conn_new = MySQLdb.connect(host='10.199.128.61', port=3309, user='vis', passwd='vispvip', db='vip_vis_stockservice', cursorclass=MySQLdb.cursors.DictCursor, charset='utf8')
    cur_old = conn_old.cursor()
    cur_new = conn_new.cursor()
    k = read_excel('E:\\osp\\11.xlsx')
    if 'barcode' in list(session.keys()):
        cur_new.execute('select * from stock_applications where stock_application_no=%s' % session['barcode'])
        new_data0 = cur_new.fetchone()
        cur_old.execute('select * from normality_sell_stocks_change_log where apply_no=%s' % session['barcode'])
        s = []
        old_data0 = cur_old.fetchone()
        s.append('SELECT nomal_change_id, SUM( CASE WHEN frozen_num < 0 THEN frozen_num ELSE 0 END ) AS minus_done_boxs_total, SUM( CASE WHEN frozen_num > 0 THEN frozen_num ELSE 0 END ) AS plus_done_boxs_total, SUM( CASE WHEN num < 0 THEN num ELSE 0 END ) AS minus_change_boxs_total, SUM( CASE WHEN num > 0 THEN num ELSE 0 END ) AS plus_change_boxs_total, COUNT(DISTINCT item_code) AS change_goods_total FROM normality_sell_stocks_change_detail WHERE nomal_change_id IN (%s) AND is_deleted = 0 GROUP BY nomal_change_id' % old_data0['id'])
        cur_old.execute(s[0])
        ji_data0 = cur_old.fetchone()
        if new_data0 == None or old_data0 == None or ji_data0 == None:
            pass
        else:
            for i in k.data0:
                if i[0].strip() in list(new_data0.keys()):
                    i.insert(1, new_data0[i[0].strip()])
                if i[2].split('*')[0].strip() in list(old_data0.keys()):
                    i.insert(3, old_data0[i[2].strip()])
                elif i[2].split('*')[0].strip() in list(ji_data0.keys()):
                    i.insert(3, ji_data0[i[2].split('*')[0].strip()])
                else:
                    i.insert(3, 'no data')

    else:
        for i in k.data0:
            i.insert(1, 'no data')
            i.insert(3, 'no data')

    if 'barcode' in list(session.keys()):
        cur_new.execute('select * from stock_application_details where stock_application_no=%s' % session['barcode'])
        new_data1 = cur_new.fetchone()
        cur_old.execute('SELECT * FROM normality_sell_stocks_change_detail WHERE item_code="%s" and  nomal_change_id IN (SELECT id FROM normality_sell_stocks_change_log WHERE apply_no=%s ) ORDER BY id DESC' % (new_data1['barcode'], session['barcode']))
        old_data1 = cur_old.fetchone()
        old_data1.pop('vendor_name')
        old_data1.pop('vendor_code')
        cur_old.execute('select * from normality_sell_goods where flagship_id=%s and goods_barcodes="%s"' % (old_data1['flagship_id'], old_data1['item_code']))
        ji_data1 = cur_old.fetchone()
        ji_data1.pop('vendor_name')
        ji_data1.pop('vendor_code')
        cur_old.execute('select * from normality_sell_stocks_change_log where apply_no=%s' % session['barcode'])
        s = cur_old.fetchone()
        ji1_data1 = {}
        ji1_data1['vendor_name'] = s['vendor_name']
        ji1_data1['vendor_code'] = s['vendor_code']
        ji1_data1['apply_no'] = s['apply_no']
        cur_old.execute('select * from vendor_shop_schedule where shop_code=%s AND warehouse="%s"' % (old_data1['flagship_id'], old_data1['sell_area']))
        s = cur_old.fetchone()
        ji1_data1['schedule_id'] = s['schedule_id']
        cur_old.execute('SELECT * FROM purchase_agreement_goods  WHERE barcode="%s" limit 1' % new_data1['barcode'])
        s = cur_old.fetchone()
        ji1_data1['v_sku_id'] = s['v_sku_id']
        if new_data1 == None or old_data1 == None or ji_data1 == None:
            pass
        else:
            for i in k.data1:
                if i[0].strip() in list(new_data1.keys()):
                    i.insert(1, new_data1[i[0].strip()])
                if i[2].split('*')[0].strip() in list(old_data1.keys()):
                    i.insert(3, old_data1[i[2].strip()])
                elif i[2].strip() in list(ji_data1.keys()):
                    i.insert(3, ji_data1[i[2].strip()])
                elif i[2].strip() in list(ji1_data1.keys()):
                    i.insert(3, ji1_data1[i[2].strip()])
                else:
                    i.insert(3, 'no data')

    else:
        for i in k.data1:
            i.insert(1, 'no data')
            i.insert(3, 'no data')

    if 'barcode' in list(session.keys()):
        cur_new.execute('select * from stock_product_status where stock_application_no=%s' % session['barcode'])
        new_data2 = cur_new.fetchone()
        cur_old.execute('SELECT * FROM visAdmin.normality_sell_goods WHERE goods_barcodes="%s" and nomal_change_id IN (SELECT id FROM visAdmin.normality_sell_stocks_change_log WHERE apply_no=%s) ORDER BY id DESC' % (new_data2['barcode'], session['barcode']))
        old_data2 = cur_old.fetchone()
        if new_data2 == None or old_data2 == None:
            pass
        else:
            for i in k.data2:
                if i[0].strip() in list(new_data2.keys()):
                    i.insert(1, new_data2[i[0].strip()])
                if i[2].split('*')[0].strip() in list(old_data2.keys()):
                    i.insert(3, old_data2[i[2].strip()])
                else:
                    i.insert(3, 'no data')

    else:
        for i in k.data2:
            i.insert(1, 'no data')
            i.insert(3, 'no data')

    return render_template('/simple_page/tabs_kaifa.html', b=k.table0, value=k.data0, b1=k.table1, value1=k.data1, b2=k.table2, value2=k.data2)
    return


@app.route('/yansql', methods=['GET', 'POST'])
def yan_sql():
    session['barcode'] = request.form['barcode']
    return jsonify(a='1')


from .lenove_jie_kou.ceshi_no import *

@app.route('/signal_run', methods=['POST', 'GET'])
@ceshi_no
def signal_run():
    pass


@app.route('/piliang_run_over', methods=['POST', 'GET'])
def piliang_run_over():
    ip = request.headers.get('X-Real-IP')
    db = sqlite3.connect(current_app.config.get('JIE_KOU'))
    cu = db.cursor()
    if request.method == 'POST':
        cu.execute('update jiekou_mulu set run_statu="2" where ip=? and statu=?', (
         request.form['ip'], '批量'))
        db.commit()
        db.close()
        return jsonify(statu='update_success')
    if request.method == 'GET':
        run_status, run_time = None, None
        run_statu_data = cu.execute('select run_statu from  jiekou_mulu  where ip=? and statu=?', (
         request.headers.get('X-Real-IP'), '批量')).fetchall()
        if run_statu_data:
            run_statu = run_statu_data[0][0]
        run_time_data = cu.execute('select update_time from  jiekou_mulu  where ip=? and statu=?', (
         request.headers.get('X-Real-IP'), '批量')).fetchall()
        if run_time_data:
            run_time = time.strftime('%Y-%m-%d:  %H:%M:%S ', time.localtime(float(run_time_data[0][0])))
        return jsonify(run_statu=run_statu, run_time=run_time)


@app.route('/piliang_run_git_over', methods=['POST', 'GET'])
def piliang_run_git_over():
    ip = request.headers.get('X-Real-IP')
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    if request.method == 'POST':
        cu.execute('update dingshi_run set statu="3" where id=? ', (
         request.form['id'],))
        db.commit()
        db.close()
        return jsonify(statu='update_success')
    if request.method == 'GET':
        run_statu = cu.execute('select run_statu from  jiekou_mulu  where ip=? and statu=?', (
         request.headers.get('X-Real-IP'), '批量')).fetchall()[0][0]
        run_time = cu.execute('select update_time from  jiekou_mulu  where ip=? and statu=?', (
         request.headers.get('X-Real-IP'), '批量')).fetchall()[0][0]
        run_time = time.strftime('%Y-%m-%d:  %H:%M:%S ', time.localtime(float(run_time)))
        return jsonify(run_statu=run_statu, run_time=run_time)


@app.route('/uplate_jiekou_list', methods=['GET', 'POST'])
def uplate_jiekou_list():
    hostname = socket.gethostname()
    webserver_ip = socket.gethostbyname(hostname)
    if request.method == 'GET':
        if 'yidi_mulu_ip' not in list(session.keys()):
            session['yidi_mulu_ip'] = '127.0.0.1'
        if session['yidi_mulu_ip'] == request.headers.get('X-Real-IP'):
            yizhi = 1
        else:
            yizhi = 0
        if 'mulu_detail' in session:
            res = session['mulu_detail']
            return render_template('/hualala/pages/jiekou_list.html', yewu_name=res['yewu_name'], ip_server=session['yidi_mulu_ip'], select_huanjing=res['select_huanjing'], huanjing=res['huanjing'], all_mulu=res['gen_mulu'], yizhi=yizhi, local_port=current_app.config.get('LOCAL_SERVER_PORT'))
        return render_template('/hualala/pages/jiekou_list.html', yewu_name='', select_huanjing='', huanjing='', all_mulu='', yizhi=yizhi, local_port=current_app.config.get('LOCAL_SERVER_PORT'))
    db = sqlite3.connect(current_app.config.get('JIE_KOU'))
    cu = db.cursor()
    if 'ip_dizhi' in list(request.form.keys()):
        session['yidi_mulu_ip'] = request.form['ip_dizhi']
        ip_dizhi = request.form['ip_dizhi']
        if ip_dizhi == webserver_ip:
            ip_dizhi = '127.0.0.1'
        mulu = cu.execute('select  mulu from jiekou_mulu where ip=? and statu=?', (ip_dizhi, '批量')).fetchall()
        url = 'http://' + ip_dizhi.strip() + ':' + current_app.config.get('LOCAL_SERVER_PORT') + '/mulu_detail'
        if len(mulu) == 0:
            return render_template('/hualala/pages/jiekou_list.html', yewu_name='', select_huanjing='', huanjing='', all_mulu='', local_port=current_app.config.get('LOCAL_SERVER_PORT'))
        mulu = mulu[0][0]
    else:
        session['yidi_mulu_ip'] = request.headers.get('X-Real-IP')
        mulu = request.form['mulu']
        ip = request.headers.get('X-Real-IP')
        if len(cu.execute('select * from jiekou_mulu where ip=? and statu=?', (
         request.headers.get('X-Real-IP'), '批量')).fetchall()) > 0:
            cu.execute('update jiekou_mulu set mulu=?,update_time=?,run_statu="0" where ip=? and statu=?', (
             request.form['mulu'], str(time.time()), request.headers.get('X-Real-IP'), '批量'))
        else:
            cu.executemany('INSERT INTO jiekou_mulu VALUES (null,?,?,?,?,?)', [
             (
              '批量', request.form['mulu'], request.headers.get('X-Real-IP'), str(time.time()), '0')])
        url = 'http://' + request.headers.get('X-Real-IP') + ':' + current_app.config.get('LOCAL_SERVER_PORT') + '/mulu_detail'
    db.commit()
    db.close()
    mulu = mulu.encode('utf-8')
    if 'huanjing' in list(request.form.keys()):
        session['huanjing'] = request.form['huanjing']
    else:
        if 'huanjing' not in list(session.keys()):
            session['huanjing'] = ''
        test_data = {'mulu': mulu, 'huanjing': session['huanjing'].encode('utf-8')}
        test_data_urlencode = urllib.parse.urlencode(test_data)
        req = urllib.request.Request(url=url, data=test_data_urlencode)
        try:
            res_data = json.loads(urllib.request.urlopen(req).read())
        except:
            return '找不到相应服务或目录'
        else:
            if 'error_detail' in list(res_data.keys()):
                return res_data['error_detail']

        if 'statu' in list(res_data.keys()) and res_data['statu'] == 'no dir':
            return '目录不存在'
    res = json.loads(res_data['data'])
    if session['huanjing'].strip() != '':
        res['select_huanjing'] = session['huanjing']
    res['gen_mulu'] = mulu.decode('utf-8')
    session['mulu_detail'] = res
    if session['yidi_mulu_ip'] == request.headers.get('X-Real-IP'):
        yizhi = 1
    else:
        yizhi = 0
    print(999999999999999999999999999999)
    print(res['gen_mulu'])
    resp = make_response(render_template('/hualala/pages/jiekou_list.html', ip_server=session['yidi_mulu_ip'], yewu_name=res['yewu_name'], select_huanjing=res['select_huanjing'], huanjing=res['huanjing'], all_mulu=res['gen_mulu'], yizhi=yizhi, local_port=current_app.config.get('LOCAL_SERVER_PORT')))
    return resp


from .lenove_jie_kou.run_jiekou import *

@app.route('/jie_kou_result', methods=['POST', 'GET'])
@jiekou_result
def jiek_result():
    pass


from .lenove_jie_kou.jiekou_list import jiekou_list_show

@app.route('/jiekou_list', methods=['POST', 'GET'])
@jiekou_list_show
def jiekou_list_show():
    pass


from .lenove_jie_kou.jiekou_list import jiekou_result_run

@app.route('/simple_jie_kou_run', methods=['POST', 'GET'])
@jiekou_result_run
def jiekou_list_showeeaa():
    pass


from .lenove_jie_kou.change_config import change_config

@app.route('/read_configparse', methods=['POST', 'GET'])
@change_config
def jiekou_list_showeeaa():
    pass


from .lenove_jie_kou.jiekou_list import *

@app.route('/jiaobenshuru', methods=['POST'])
@jiaobenshuru
def jiaoben_shuru():
    pass


@app.route('/shishitiaoshi', methods=['GET', 'POST'])
@shishitiaoshi
def shishitiaoshi():
    pass


@app.route('/jiekou_mulu', methods=['GET', 'POST'])
@url_insert
def jiekou_mulu():
    pass


@app.route('/get_mulu', methods=['GET', 'POST'])
@get_mulua
def get_mulua():
    pass


@app.route('/piliang_run', methods=['GET', 'POST'])
@piliang_run
def piliang_run():
    pass


@app.route('/piliang_run_result', methods=['GET', 'POST'])
@piliang_run_resulttt
def piliang_run_result():
    pass


@app.route('/piliang_git_result', methods=['GET', 'POST'])
@piliang_git_result
def piliang_git_result():
    pass


@app.route('/jie_kou_result', methods=['GET', 'POST'])
def jie_kou_result():
    return jsonify(a='1')


from .lenove_jie_kou.run_jiekou import *

@app.route('/jie_kou', methods=['POST', 'GET'])
@piliangjiekou_result
def run_jiekou():
    pass


@app.route('/jiekou_page', methods=['GET', 'POST'])
@jiekou_piliang
def jiekou_page():
    pass


from .hualala.moke_dangban import moke_dangban

@app.route('/moke_dangban', methods=['GET', 'POST'])
@moke_dangban
def moke_dangban():
    pass


from .hualala.moke_dangban import add_case

@app.route('/add_case', methods=['GET', 'POST'])
@add_case
def add_case():
    pass


from .hualala.moke_dangban import case_read

@app.route('/case_read', methods=['GET', 'POST'])
@case_read
def case_read():
    pass


from .hualala.moke_dangban import bianji_case

@app.route('/bianji_case', methods=['GET', 'POST'])
@bianji_case
def bianji_case():
    pass


from .hualala.moke_dangban import yewu_bianji_show

@app.route('/yewu_bianji_show', methods=['GET', 'POST'])
@yewu_bianji_show
def yewu_bianji_show():
    pass


from .hualala.moke_dangban import linux_add

@app.route('/linux_add', methods=['GET', 'POST'])
@linux_add
def linux_add():
    pass


from .hualala.moke_dangban import top_add_ceshi

@app.route('/top_add', methods=['GET', 'POST'])
@top_add_ceshi
def top_add_ceshi():
    pass


from .hualala.moke_dangban import moke_return

@app.route('/moke_return/<id>', methods=['GET', 'POST'])
@moke_return
def moke_return(id):
    pass


from .hualala.moke_dangban import yewuadd

@app.route('/yewu_add', methods=['GET', 'POST'])
@yewuadd
def yewuadd():
    pass


from .hualala.moke_dangban import server_use

@app.route('/server_use', methods=['GET', 'POST'])
@server_use
def server_use():
    pass


from .hualala.moke_dangban import delete_moke_xiangmu

@app.route('/delete_moke_xiangmu', methods=['GET', 'POST'])
@delete_moke_xiangmu
def top_add_ceshi():
    pass


@app.route('/<name>', methods=['GET', 'POST'])
def top_add_ceshi(name):
    return jsonify(statu=name)


@app.route('/first_page', methods=['GET', 'POST'])
def first_page_exe():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    name = cu.execute('select name from user where ip="%s" order by time desc limit 0,1' % request.headers.get('X-Real-IP')).fetchall()
    if len(name) == 0:
        return redirect(url_for('login_new'))
    name = name[0][0]
    if request.method == 'GET':
        git_detail = [ list(i) for i in cu.execute('select * from git_detail  ').fetchall() ]
        for i in git_detail:
            i[3] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(i[3])))

        email_detail = [ i[0] for i in cu.execute('select address from email_address where user="%s"' % name).fetchall() ]
        fajianren = [ i[0] for i in db.execute('select email_user from fajianren where name="%s"' % name).fetchall() ]
        dingshi_detail = [ [i[1], i[2], i[4], i[6]] for i in cu.execute('select * from dingshi_run where name="%s" order by update_time desc ' % name).fetchall() ]
        jobs = [ i[0] for i in db.execute('select job_name from jekins where name="%s"' % name).fetchall() ]
        for k, i in enumerate(dingshi_detail):
            i.insert(0, i[0])
            i[1] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(i[0])))
            if i[(-2)].strip() == '0':
                i[-2] = 'ready'
            elif i[(-2)].strip() == '1':
                i[-2] = 'running'
            elif i[(-2)].strip() == '2':
                i[-2] = 'over'

        time_date = time.strftime('%Y-%m-%d ', time.localtime(time.time()))
        server_detail = [ i[1] for i in cu.execute('select * from all_server where statu="1"').fetchall() ]
        db.close()
        return render_template('/hualala/pages/index.html', git_detail=git_detail, email_detail=email_detail, time_date=time_date, dingshi_detail=dingshi_detail, fajianren=fajianren, jobs=jobs, server_detail=server_detail)
    git_url = request.form['git'].strip()
    git_beizhu = request.form['beizu'].strip()
    git_branch = request.form['branch'].strip()
    if git_url.strip() != '' and git_beizhu.strip() != '':
        cu.executemany('INSERT INTO git_detail VALUES (?,?,?,?,?,?)', [
         (
          git_url, git_beizhu, name, str(time.time()), '', git_branch)])
        db.commit()
        db.close()
    return jsonify(a='1')


@app.route('/login', methods=['GET', 'POST'])
def login_new():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    if request.method == 'GET':
        db.close()
        return render_template('/hualala/login.html')
    ip = request.headers.get('X-Real-IP')
    name = request.form['name']
    passs = request.form['password']
    user_check = cu.execute('select * from user where name="%s" and pass="%s" ' % (name, passs)).fetchall()
    if len(user_check) != 0:
        cu.execute('update  user  set ip="" where ip=?', [ip])
        db.commit()
        cu.executemany('update  user  set time=? ,ip=? where name=?', [(time.time(), ip, name)])
        db.commit()
        response = make_response(redirect(url_for('chongou_test')))
        response.set_cookie('flask_login', 'a')
        db.close()
        print(response.headers, response.status, response.get_data())
        return response
    db.close()
    return render_template('/hualala/login.html')


from .hualala.user import *

@app.route('/user_manage', methods=['GET', 'POST'])
@user
def user_manage():
    pass


@app.route('/server_manage', methods=['GET', 'POST'])
@server
def server_manage():
    pass


@app.route('/change_server', methods=['GET', 'POST'])
def change_server():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    if request.form['statu'] == 'true':
        statu = '0'
    else:
        statu = '1'
    cu.executemany('update   all_server set statu=? where id=?', [(statu, int(request.form['change_id']))])
    db.commit()
    db.close()
    return jsonify(a=1)


@app.route('/add_server', methods=['GET', 'POST'])
def add_server():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    if request.form['ip'].strip() == '' or request.form['duankou'].strip() == '':
        return jsonify(a='输入不能为空')
    if len(cu.execute('select * from all_server where ip="%s"' % request.form['ip']).fetchall()) > 0:
        return jsonify(a='server ip 已经存在')
    cu.executemany('INSERT INTO  all_server values (null,?,?,?,?)', [(request.form['ip'], request.form['duankou'], '0', '0')])
    db.commit()
    db.close()
    return jsonify(a=1)


from .hualala.run import *

@app.route('/run_hualala', methods=['GET', 'POST'])
@run_hualala
def run_hual():
    pass


from .hualala.run import *

@app.route('/run_charge', methods=['GET', 'POST'])
@run_charge
def run_hual():
    pass


@app.route('/delete_ben', methods=['GET', 'POST'])
def delete_ben():
    tongji_db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    tongji_cu = tongji_db.cursor()
    if request.form['statu'] == 'url':
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
    else:
        db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu = db.cursor()
    ip = request.headers.get('X-Real-IP')
    name = request.form['name'].strip()
    branch = request.form['branch'].strip()
    git = request.form['git'].strip()
    cu.execute('delete from git_detail  where  name="%s"  and submit= "%s"  and  branch= "%s"  ' % (git, name, branch)).fetchall()
    db.commit()
    tongji_cu.execute('delete from ci_tongji  where  git_url="%s"  and branch= "%s"' % (git, branch)).fetchall()
    tongji_db.commit()
    db.commit()
    tongji_db.close()
    db.close()
    return jsonify(statu='success')


from .hualala.add_email import *

@app.route('/add_email', methods=['GET', 'POST'])
@add_email
def add_email():
    pass


@app.route('/emali_list_all', methods=['GET', 'POST'])
@show_email
def emali_list():
    pass


@app.route('/delete_email', methods=['GET', 'POST'])
@delete_email
def emali_list():
    pass


@app.route('/send_emali', methods=['GET', 'POST'])
@send_emali
def send_emali():
    pass


@app.route('/add_file_detail', methods=['GET', 'POST'])
@add_file_detail
def add_file_detail():
    pass


@app.route('/dingshi_result/<id>', methods=['GET', 'POST'])
def dingshi_result(id):
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    url_detail = 'http://' + socket.gethostbyname(socket.gethostname()) + ':5021' + url_for('dingshi_result', id=id)
    if str(id).strip() == 'shishi':
        z = cu.execute('select run_result from dingshi_run where id=?', id.fetchall()[0][0])
        timee = cu.execute('select update_time,last_run_time from dingshi_run where id=?', id).fetchall()[0]
    else:
        z = cu.execute('select run_result from dingshi_run where id=?', (id,)).fetchall()[0][0]
        timee = cu.execute('select update_time,last_run_time from dingshi_run where  id=?', (id,)).fetchall()[0]
        z = json.loads(z)
    job = json.loads(cu.execute('select job from dingshi_run where id=?', (id,)).fetchall()[0][0])
    if 'name' in list(job.keys()) and 'no select' != job['name'].strip():
        job_r = job['name'] + ':' + job['result']
    else:
        job_r = 'null'
    run_taken = float(job['end_time'])
    if run_taken > 60:
        run_time_detail = str(int(run_taken) / 60) + '分' + str(int(run_taken) % 60) + '秒'
    else:
        run_time_detail = str(int(run_taken)) + '秒'
    total = [
     0, 0, 0, 0]
    timeArray = time.localtime(float(timee[0]))
    otherStyleTime = time.strftime('%H:%M:%S', timeArray)
    timee = list(timee)
    if timee[1].strip() == '':
        timee[1] = time.strftime('%Y:%m:%d', timeArray)
    timee = timee[1] + '   ' + otherStyleTime
    for k in z:
        total[0] += z[k]['count']
        total[1] += z[k]['Pass']
        total[2] += z[k]['fail']
        total[3] += z[k]['error']

    db.close()
    return render_template('/hualala/pages/test_result.html', time=str(time.time()), z=z, total=total, timee=timee, job=job_r, taken=run_time_detail, url_detail=url_detail)


from .hualala.yunxing_tongji import pic_yewu_email

@app.route('/jiekou_result/<id>', methods=['GET', 'POST'])
def jiekou_result(id):
    ursr_idid = id
    ip = request.headers.get('X-Real-IP')
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    url_detail = 'http://' + socket.gethostbyname(socket.gethostname()) + ':5025' + url_for('jiekou_result', id=id)
    if request.method == 'GET':
        s_assert = assert_run()
        data = cu.execute('select * from  dingshi_run where id=?', (id,)).fetchall()[0]
        tim = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data[1])))
        all = []
        top_all = {}
        taken_time = int(json.loads(data[10])['end_time'])
        job_result = json.loads(data[10])['result']
        if job_result.strip() == '':
            job_result = 'NULL'
        if taken_time >= 60:
            fen = taken_time / 60
            miao = taken_time % 60
            taken_time = '%s分   %s秒' % (fen, miao)
        else:
            taken_time = '%s秒' % taken_time
        taken_time = taken_time.decode('utf-8')
        all_result = json.loads(data[8])
        qll_fail = 0
        all_succ = 0
        yewuxian_detail = {}
        if len(all_result) != 0:
            for i in all_result:
                name, git_beizhu = i.split('##')
                detail = []
                statu = 0
                fail = 0
                succ = 0
                count = len(json.loads(all_result[i]))
                for k, z in json.loads(all_result[i]).items():
                    result = json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(z['respons']))), parse_int=int), indent=4, sort_keys=False, ensure_ascii=False)
                    id = int(k)
                    req_url = z['req_url']
                    if type(z['case_assert']) in ('str', 'unicode') and z['case_assert'].strip() != '':
                        assert_data = json.loads(z['case_assert'])
                    else:
                        assert_data = ''
                    case_assert = json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(assert_data))), parse_int=int), indent=4, sort_keys=False, ensure_ascii=False)
                    comment = z['case_name']
                    req = z['req']
                    req = json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(req))), parse_int=int), indent=4, sort_keys=False, ensure_ascii=False)
                    if z['assert_result'] == False:
                        statu = 1
                        fail += 1
                        qll_fail += 1
                        detail.append(['failCase', id, comment, case_assert, result, req, req_url])
                    else:
                        succ += 1
                        all_succ += 1
                        detail.append(['passCase', id, comment, case_assert, result, req, req_url])

                detail = sorted(detail, key=lambda x: x[1])
                if git_beizhu not in list(yewuxian_detail.keys()):
                    yewuxian_detail[git_beizhu] = {'success': 0, 'fail': 0, 'count': 0, 'all': 0}
                if git_beizhu not in list(top_all.keys()):
                    top_all[git_beizhu] = {'success': 0, 'fail': 0, 'count': 0, 'all': []}
                if statu == 1:
                    top_all[git_beizhu]['all'].append([name, 'failClass', [count, succ, fail, count], detail])
                    top_all[git_beizhu]['success'] = top_all[git_beizhu]['success'] + int(succ)
                    top_all[git_beizhu]['fail'] = top_all[git_beizhu]['fail'] + int(fail)
                    top_all[git_beizhu]['count'] = top_all[git_beizhu]['count'] + int(count)
                    yewuxian_detail[git_beizhu]['success'] = yewuxian_detail[git_beizhu]['success'] + int(succ)
                    yewuxian_detail[git_beizhu]['fail'] = yewuxian_detail[git_beizhu]['fail'] + int(fail)
                    yewuxian_detail[git_beizhu]['count'] = yewuxian_detail[git_beizhu]['count'] + int(count)
                    yewuxian_detail[git_beizhu]['all'] = yewuxian_detail[git_beizhu]['all'] + 1
                elif statu == 0:
                    top_all[git_beizhu]['all'].append([name, 'passClass', [count, succ, fail, count], detail])
                    top_all[git_beizhu]['success'] = top_all[git_beizhu]['success'] + int(succ)
                    top_all[git_beizhu]['fail'] = top_all[git_beizhu]['fail'] + int(fail)
                    top_all[git_beizhu]['count'] = top_all[git_beizhu]['count'] + int(count)
                    yewuxian_detail[git_beizhu]['success'] = yewuxian_detail[git_beizhu]['success'] + int(succ)
                    yewuxian_detail[git_beizhu]['fail'] = yewuxian_detail[git_beizhu]['fail'] + int(fail)
                    yewuxian_detail[git_beizhu]['count'] = yewuxian_detail[git_beizhu]['count'] + int(count)
                    yewuxian_detail[git_beizhu]['all'] = yewuxian_detail[git_beizhu]['all'] + 1

        db.close()
        hostname = socket.gethostname()
        pic_url = os.path.join('http://' + socket.gethostbyname(hostname) + ':5025/static/result_pic', str(ursr_idid) + '.png')
        session['take_result'] = yewuxian_detail
        if len(all_result) != 0:
            pic_yewu_email(ursr_idid)
        return render_template('/hualala/jiekou_test/test_result.html', z=top_all, time=tim, result_url=url_detail, taken_time=taken_time, fail=qll_fail, success=all_succ, job_result=job_result, pic_url=pic_url, request_statu=request.args.get('statu'))


@app.route('/open_dingshi_detail', methods=['GET', 'POST'])
@open_dingshi_detail
def open_dingshi_detail():
    pass


@app.route('/add_fajianren', methods=['GET', 'POST'])
@add_fajianren
def add_fajianren():
    pass


@app.route('/show_fajianren', methods=['GET'])
@show_fajianren
def show_fajianren():
    pass


@app.route('/delete_fajianren', methods=['GET'])
@delete_fajianren
def delete_fajianren():
    pass


@app.route('/add_jekins', methods=['GET', 'POST'])
@add_jekins
def add_fajianren():
    pass


@app.route('/jekins_list', methods=['GET', 'POST'])
@jekins_list
def jekins_list():
    pass


@app.route('/jekins_delete', methods=['GET', 'POST'])
@jekins_delete
def jekins_delete():
    pass


@app.route('/suite_delete', methods=['GET', 'POST'])
@suite_delete
def suite_delete():
    pass


@app.route('/xiaomin', methods=['GET', 'POST'])
def xiaomin():
    a = 222
    return jsonify(statu='success')


@app.route('/second_page', methods=['GET', 'POST'])
def second():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    name = cu.execute('select name from user where ip="%s" order by time desc limit 0,1' % request.headers.get('X-Real-IP')).fetchall()
    if len(name) == 0:
        return redirect(url_for('login_new'))
    name = name[0][0]
    data = cu.execute('select * from locust_file order by id desc').fetchall()
    db.close()
    return render_template('/hualala/pages/second_page.html', data=data)


@app.route('/teach', methods=['GET', 'POST'])
def teach():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    db.close()
    return render_template('/hualala/pages/texch.html')


from .hualala.locust_fiel import upload_fil

@app.route('/upload_file', methods=['GET', 'POST'])
@upload_fil
def upload_file():
    pass


from .hualala.locust_fiel import upload_fil_beizu

@app.route('/upload_fil_beizu', methods=['GET', 'POST'])
@upload_fil_beizu
def upload_file():
    pass


from .lenove_jie_kou.run_jiekou import jiekou_gitce

@app.route('/jiekou_yun', methods=['GET', 'POST'])
@jiekou_gitce
def jiekou_git():
    pass


from .lenove_jie_kou.run_jiekou import guanlian_ip_dizhi

@app.route('/guanlian_ip', methods=['GET', 'POST'])
@guanlian_ip_dizhi
def guanlian_ip():
    pass


from .lenove_jie_kou.run_jiekou import debugging

@app.route('/debugging', methods=['GET', 'POST'])
@debugging
def run_dubbing():
    pass


from .lenove_jie_kou.jekins import signal_job_detail

@app.route('/signal_job_detail', methods=['GET', 'POST'])
@signal_job_detail
def signal_job_detail():
    pass


from .lenove_jie_kou.jekins import job_gengxin

@app.route('/job_gengxin', methods=['GET', 'POST'])
@job_gengxin
def job_gengxin():
    pass


from .lenove_jie_kou.jekins import delete_server

@app.route('/delete_server', methods=['GET', 'POST'])
@delete_server
def delete_server():
    pass


from .hualala.run import change_run_statu

@app.route('/change_run_statu', methods=['POST'])
@change_run_statu
def change_run_statu():
    pass


from .hualala.run import update_host

@app.route('/updata_html', methods=['POST'])
@update_host
def update_host22():
    pass


from .hualala.submit_git import submit_git

@app.route('/get_file_git', methods=['POST'])
@submit_git
def get_file_git():
    pass


from .hualala.submit_git import get_sumint_statu

@app.route('/get_sumint_statu', methods=['POST'])
@get_sumint_statu
def get_sumint_statu():
    pass


from .hualala.yunxing_tongji import yunxing_tongji

@app.route('/yunxing_tongji', methods=['POST'])
@yunxing_tongji
def yunxing_tongji():
    pass


from .hualala.yunxing_tongji import test_image

@app.route('/test_image/<id>', methods=['POST', 'GET'])
@test_image
def test_image(id):
    pass


from .hualala.yunxing_tongji import pic_yewu_today

@app.route('/pic_yewu_oday/<testid>', methods=['POST', 'GET'])
@pic_yewu_today
def pic_yewu_today(testid):
    pass


from .hualala.yunxing_tongji import pic_yewu_today_email

@app.route('/pic_yewu_today_email', methods=['POST', 'GET'])
@pic_yewu_today_email
def pic_yewu_today_email():
    pass


from .hualala.yunxing_tongji import tongji_mail

@app.route('/tongji_mail', methods=['POST', 'GET'])
@tongji_mail
def tongji_mail():
    pass


from .hualala.user import add_user_team

@app.route('/add_user_team', methods=['POST', 'GET'])
@add_user_team
def add_user_team():
    pass


from .hualala.user import gengxin_team

@app.route('/gengxin_team', methods=['POST', 'GET'])
@gengxin_team
def gengxin_team():
    pass


from .hualala.yunxing_tongji import local_tongji_seven

@app.route('/local_seven_today', methods=['POST', 'GET'])
@local_tongji_seven
def local_tongji_seven():
    pass


from .hualala.yunxing_tongji import local_seven_pic

@app.route('/local_seven_pic/<testid>', methods=['POST', 'GET'])
@local_seven_pic
def local_seven_pic(testid):
    pass


from .hualala.yunxing_tongji import local_tongji_today

@app.route('/local_today_today', methods=['POST', 'GET'])
@local_tongji_today
def local_tongji_today():
    pass


from .hualala.yunxing_tongji import local_today_pic

@app.route('/local_today_pic/<testid>', methods=['POST', 'GET'])
@local_today_pic
def local_today_pic(testid):
    pass


from .hualala.save_log_jiequ import save_log_jiequ

@app.route('/save_log_jiequ', methods=['POST', 'GET'])
@save_log_jiequ
def save_log_jiequ():
    pass


@app.route('/plot.png')
def plot():
    from io import BytesIO
    import base64, matplotlib.pyplot as plt
    fig = plt.figure(figsize=(1, 1))
    sio = BytesIO()
    fig.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)


from .hualala.appium_server import appium_server

@app.route('/appium_server', methods=['GET', 'POST'])
@appium_server
def appium_server():
    pass


@app.route('/local_ui_test', methods=['GET', 'POST'])
def local_ui_test():
    return render_template('/hualala/pages/local_ui_test.html', port=current_app.config.get('LOCAL_SERVER_PORT'))


@app.route('/open_window_page_result', methods=['GET', 'POST'])
def open_window_page_result():
    return render_template('/hualala/pages/local_ui_result.html', port=current_app.config.get('LOCAL_SERVER_PORT'))


from .jmeter_log.jmeter_log import jemter_add_linux

@app.route('/jemter_add_linux', methods=['GET', 'POST'])
@jemter_add_linux
def jemter_add_linux():
    pass


from .jmeter_log.jmeter_log import jemter_get_all_linux

@app.route('/jemter_get_all_linux', methods=['GET', 'POST'])
@jemter_get_all_linux
def jemter_get_all_linux():
    pass


from .jmeter_log.jmeter_log import delete_simple_linux

@app.route('/delete_simple_linux', methods=['GET', 'POST'])
@delete_simple_linux
def delete_simple_linux():
    pass


from .jmeter_log.jmeter_log import run_linux

@app.route('/run_linux', methods=['GET', 'POST'])
@run_linux
def run_linux():
    pass


from .jmeter_log.jmeter_log import bianji_linux

@app.route('/bianji_linux', methods=['GET', 'POST'])
@bianji_linux
def bianji_linux():
    pass


from .jmeter_log.jmeter_log import stop_run_linux

@app.route('/stop_run_linux', methods=['GET', 'POST'])
@stop_run_linux
def stop_run_linux():
    pass


@app.route('/nmon_log', methods=['GET', 'POST'])
def nmon_log():
    return render_template('/nmon_jmeter/base.html')


@app.route('/run_jiankong', methods=['GET', 'POST'])
def run_jiankong():
    json_data = json.loads(request.get_data())
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for i in json_data:
        ip = i
        name = json_data[i]['name']
        password = json_data[i]['password']
        port = int(json_data[i]['port'])
        ssh.connect(ip, port, name, password)
        stdin, stdout, stderr = ssh.exec_command('我的命令')
        ssh.close()

    return jsonify(statu='run_success')


from .hualala.phone import phone_changliang_add

@app.route('/phone_changliang_add', methods=['GET', 'POST'])
@phone_changliang_add
def phone_changliang_add():
    pass


from .hualala.phone import add_phone_modal

@app.route('/add_phone_modal', methods=['GET', 'POST'])
@add_phone_modal
def add_phone_modal():
    pass


from .hualala.phone import bianji_phone_modal

@app.route('/bianji_phone_modal', methods=['GET', 'POST'])
@bianji_phone_modal
def bianji_phone_modal():
    pass


from .hualala.phone import shouye

@app.route('/zichan_shouye', methods=['GET', 'POST'])
@shouye
def shouye():
    pass


from .hualala.phone import phone_changliang_delete

@app.route('/phone_changliang_delete', methods=['GET', 'POST'])
@phone_changliang_delete
def phone_changliang_delete():
    pass


from .hualala.phone import phone_simple_caozuo

@app.route('/phone_simple_caozuo/<name>', methods=['GET', 'POST'])
@phone_simple_caozuo
def phone_simple_caozuo(name):
    pass


from .hualala.phone import phone_submit

@app.route('/phone_submit', methods=['GET', 'POST'])
@phone_submit
def phone_submit():
    pass


from .hualala.phone import excel_daochu

@app.route('/daochu_phone_list', methods=['GET'])
@excel_daochu
def excel_daochu():
    pass


from .hualala.phone import all_phone_delete

@app.route('/all_phone_delete', methods=['POST'])
@all_phone_delete
def all_phone_delete():
    pass


@app.route('/get_email_detail', methods=['POST', 'GET'])
def get_email_detail():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    name = cu.execute('select name from user where ip="%s" order by time desc limit 0,1' % request.headers.get('X-Real-IP')).fetchall()
    if len(name) == 0:
        return jsonify(error_detail='未登陆，获取不到用户名')
    name = name[0][0]
    email_detail = [ i[0] for i in cu.execute('select address from email_address where user="%s"' % 'weixidong').fetchall() ]
    fajianren = [ i[0] for i in db.execute('select email_user from fajianren where name="%s"' % 'weixidong').fetchall() ]
    db.close()
    resp = jsonify(user_name='weixidong', shoujianren=email_detail, fajianren=fajianren)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


from .hualala.jiekou_fenxi import jiekou_fenxi_shouye

@app.route('/jiekou_fenxi', methods=['GET'])
@jiekou_fenxi_shouye
def jiekou_fenxi_shouye():
    pass


from .hualala.jiekou_git_chonggou import chongou_test

@app.route('/chongou_test', methods=['GET'])
@chongou_test
def chongou_test():
    pass


from .hualala.jiekou_git_chonggou import git_bianji

@app.route('/git_bianji', methods=['POST'])
@git_bianji
def git_bianji():
    pass


from .hualala.jiekou_git_chonggou import new_get_run_statu

@app.route('/new_get_run_statu', methods=['POST'])
@new_get_run_statu
def new_get_run_statu():
    pass


@app.route('/git_hengfeng_detail', methods=['POST', 'GET'])
def git_hengfeng_detail():
    data = {}
    import requests
    from datetime import datetime
    time_now = datetime.now().strftime('%Y%m%d%H%M%S')
    data['serviceName'] = 'PERSONAL_REGISTER_EXPAND'
    data['platformNo'] = '5000001104'
    data['keySerial'] = '1'
    ss = {'redirectUrl': 'http://192.168.33.216:5025/23adadff232323', 
       'platformUserNo': 'HFJYJFCR190509000065999', 
       'realName': '苏秦', 
       'checkType': 'LIMIT', 
       'idCardType': 'PRC_ID', 
       'userRole': 'INVESTOR', 
       'idCardNo': '513436200005099634', 
       'mobile': '19992131029', 
       'bankcardNo': '6222600260001072445', 
       'bankcode': 'COMM', 
       'accessType': 'FULL_CHECKED', 
       'auditStatus': 'PASSED', 
       'groupAccountNO': '', 
       'timestamp': time_now, 
       'requestNo': '19050914021912868874', 
       'code': '0', 
       'status': 'SUCCESS'}
    data['reqData'] = json.dumps(ss)
    print(data['reqData'])
    url_sing = 'http://xq-app-server.jc1.jieyue.com/xqAppServer/api/APPBizRest/sign/v1/'
    headers = {'Content-Type': 'application/json'}
    headers_sing = {'Content-Type': 'application/json'}
    headers_sing['reqJSON'] = data['reqData']
    k = requests.post(url_sing, data=data['reqData'], headers=headers_sing)
    print(8888888888888888888888888)
    print(k.text)
    k = json.loads(k.text)['responseBody']['sign']
    print(k)
    data['sign'] = k
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    dd = 'http://47.95.110.16:8096/bha-neo-app/lanmaotech/gateway'
    s = requests.post(dd, data=data, headers=headers)
    print(11111111111111111111111111111111)
    print(data)
    requestkey = s.text.split("requestKey: '")[(-1)].split("',")[0]
    print(requestkey)
    print(222222222222222)
    url_msg = 'http://47.95.110.16:8096/bha-neo-app/gateway/sms/smsForEnterprise'
    data = {'requestKey': requestkey, 
       'bizType': 'REGISTER', 
       'mobile': '19992131029'}
    s = requests.post(url_msg, data=data, headers=headers)
    print(3333333333333333333333333)
    print(s.text)
    print(44444444444444444)
    url3 = 'http://47.95.110.16:8096/bha-neo-app/gateway/mobile/personalRegisterExpand/register'
    data = {'serviceType': 'BANKCARD_AUTH', 
       'realName': '苏秦', 
       'credType': 'PRC_ID', 
       'idCardNo': '513436200005099634', 
       'maskedCredNum': '51343 ** ** ** ** ** 634', 
       'bankcardNo': '6222600260001072445', 
       'mobile': '19992131029', 
       'smsCode': '456543', 
       'smsCount': '32', 
       'password': '655126', 
       'confirmPassword': '655126', 
       'protocolCheckBox': 'false', 
       'requestKey': requestkey}
    s = requests.post(url3, data=data, headers=headers)
    return s.text


@app.route('/23adadff232323', methods=['POST', 'GET'])
def adfaffedfdfe():
    return jsonify(statu=2)


@app.route('/test_hengfeng_aa', methods=['POST', 'GET'])
def test_hengfeng_aa():
    return render_template('/1.html')


from .hualala.jiekou_git_chonggou import get_renwu_detail

@app.route('/get_renwu_detail', methods=['POST', 'GET'])
@get_renwu_detail
def get_renwu_detail():
    pass