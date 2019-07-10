# -*- coding: utf-8 -*-
from tempfile import mktemp
from app import app
from flask import send_from_directory,send_file,Response
import socket
import paramiko
import os
from hualala.check_login import  *
from hualala.git_submit import  *
import json
import urllib2
import re
import  chardet
from jie_kou import *
from functools import wraps
from zhixing import *
from data_verification import *
from yuansudingwei import *
import time
import sqlite3
from shell_name import *
from form import  *
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import datetime
import json
bootstrap = Bootstrap(app)
UPLOAD_FOLDER = 'static/Uploads'

@app.before_request
def before_request():
    g.db = sqlite3.connect(current_app.config.get('JIE_KOU'))
    g.cu=g.db.cursor()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()
'''
从这里开始是接口路由

 '''

#接口发送前向linux服务器日志写入起始内容
from lenove_jie_kou.wirte_logs import *
@app.route('/wirte_logs', methods=['POST', 'GET'])
@wirte_logs
def wirte_logs():
     pass

#demo测试
@app.route('/post', methods=['POST'])
def demo_post():
     return jsonify(a=request.form)

#demo测试
@app.route('/get', methods=['get'])
def demo_get():
     return jsonify(a=request.argv)

#读取linux日志信息
@app.route('/read_logs', methods=['POST','GET'])
def read_logs():
 ip='127.0.0.1'
 return jsonify(a=2,b=3)
 if request.method=='POST':
        linux=g.cu.execute('select linux from jie_kou_test where name="%s" and ip="%s"' % (request.form['name'],ip)).fetchall()[0][0]
        linux=eval(linux)
        hostname = linux['ip']
        username = linux['name']
        password = linux['password']
        if linux['string'].strip()=='time':
            linux['string']=datetime.datetime.now().strftime('%Y-%m-%d')
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname, 22, username, password, timeout=5)
    #获取日志目录信息
        stdin, stdout, stderr = s.exec_command(
                 'tail -n  50 ' + linux['mu_lu'])
    #logs='['+time.strftime('%Y-%m-%d',time.localtime(time.time()))+stdout.read().strip().split(time.strftime('%Y-%m-%d',time.localtime(time.time())))[-1]
        k=str(linux['string'])+str(linux['string']).join(stdout.read().strip().split(linux['string'])[int('-'+(linux['num'])):])
        g.cu.execute('UPDATE jie_kou_test SET log=?,time=? WHERE num=? and name=? and ip=?',
                     (k.decode('utf-8'),time.time(),'run', request.form['name'], ip))
        g.db.commit()
        return jsonify(data=k)
 elif request.method=='GET':
     if request.args.get('shi')=='yunxing_log':
         data= g.cu.execute('select log from jie_kou_test where name="%s" and ip="%s" and num="run"' % (
             request.args.get('name'), ip)).fetchall()[0]
         return jsonify(data=data)
     if request.args.get('shi')=='bug_log':
         data= g.cu.execute('select log from jie_kou_test where name="%s" and ip="%s" and num="bug"' % (
             request.args.get('name'), ip)).fetchall()[0]
         return jsonify(data=data)
     if request.args.get('shi')=='tiaoshi_log':
         data= g.cu.execute('select log from jie_kou_test where name="%s" and ip="%s" and num="debug"' % (
             request.args.get('name'),ip)).fetchall()[0]
         return jsonify(data=data)
#获取传过来的服务器连接信息，并保存到配置缓存中
@app.route('/linux_config', methods=['POST'])
def linux_config():
    if request.method=='POST':
        linux=request.form['linux']
        config=request.form['config']
        name=request.form['name']
        if g.cu.execute('select * from jie_kou_test where name="%s"'% name).fetchall()==[]:
           g.cu.executemany('INSERT INTO jie_kou_test VALUES (?,?,?,?,?,?,?,?)', [
            ('run', name, linux, 'no data', config, str(request.remote_addr),'no data',time.time())])
           g.db.commit()
        else:
            g.cu.execute('UPDATE jie_kou_test SET name=?,linux=?,ifconfig=?,time=? WHERE num=? and name=? and ip=?',
                         (name,linux,config,time.time(),'run',name,request.remote_addr))
            g.db.commit()
        return jsonify(da=1)
#开发调试接口页面
@app.route('/jie_run', methods=['GET','POST'])
def  jie_run():
    if request.method=="GET" :
        return render_template('/simple_page/yun_jiekou.html',data='11'
                               )
    elif request.method=="POST":
        jie_kou_test=request.form['shi']
        jie_name=request.form['name']
        data=g.cu.execute('select ifconfig from jie_kou_test where name="%s" and ip="%s"' % (jie_name,str(request.remote_addr))).fetchall()[0][0].split('\n')
        pon=kaifa_run(jie_kou_test,data)
        return jsonify(a=pon.x)


#开发调试接口页面
@app.route('/no_use', methods=['GET','POST'])
def  jie_rueen():
  return render_template('/simple_page/yun_jiekou.html')
#开发调试接口页面tabs 测试
@app.route('/tabs_kaifa', methods=['GET','POST'])
def  tabs_kaifa():
 if 'barcode'  not in session.keys() or session['barcode'].strip()=='':
        session['barcode'] = '201701221000005'
        table=['no data','no data','no data']
        data=['no data','no data','no data','no data','no data']
        return render_template('/simple_page/tabs_kaifa.html', b=table, value=data, b1=table, value1=data,
                               b2=table, value2=data)
 else:
    conn_old = MySQLdb.connect(host='10.199.128.61', port=3309, user='vis', passwd='vispvip', db='visAdmin',
                           cursorclass=MySQLdb.cursors.DictCursor,charset='utf8')
    conn_new = MySQLdb.connect(host='10.199.128.61', port=3309, user='vis', passwd='vispvip', db='vip_vis_stockservice',
                           cursorclass=MySQLdb.cursors.DictCursor,charset='utf8')
    cur_old = conn_old.cursor()
    cur_new = conn_new.cursor()
    #读取excel表格
    k=read_excel(r'E:\osp\11.xlsx')
    if 'barcode'   in session.keys():
        cur_new.execute('select * from stock_applications where stock_application_no=%s'  % session['barcode'] )
        new_data0=cur_new.fetchone()
        cur_old.execute('select * from normality_sell_stocks_change_log where apply_no=%s'  %  session['barcode'])
        s=[]
        old_data0=cur_old.fetchone()
        s.append('SELECT nomal_change_id, SUM( CASE WHEN frozen_num < 0 THEN frozen_num ELSE 0 END ) AS minus_done_boxs_total, SUM( CASE WHEN frozen_num > 0 THEN frozen_num ELSE 0 END ) AS plus_done_boxs_total, SUM( CASE WHEN num < 0 THEN num ELSE 0 END ) AS minus_change_boxs_total, SUM( CASE WHEN num > 0 THEN num ELSE 0 END ) AS plus_change_boxs_total, COUNT(DISTINCT item_code) AS change_goods_total FROM normality_sell_stocks_change_detail WHERE nomal_change_id IN (%s) AND is_deleted = 0 GROUP BY nomal_change_id' %  old_data0['id'])
        cur_old.execute(s[0])
        ji_data0=cur_old.fetchone()
        if new_data0==None  or  old_data0==None  or ji_data0==None :
            pass
        else:
          for i in k.data0:
            if i[0].strip()  in  new_data0.keys():
                i.insert(1, new_data0[i[0].strip() ])
            if i[2].split('*')[0].strip()  in  old_data0.keys():
                  i.insert(3, old_data0[i[2].strip() ])
            elif i[2].split('*')[0].strip()  in  ji_data0.keys():
                i.insert(3,  ji_data0[i[2].split('*')[0].strip()])
            else:
                i.insert(3, 'no data')
    else:
        for i in k.data0:
                i.insert(1, 'no data')
                i.insert(3, 'no data')
    if 'barcode'   in session.keys():

        cur_new.execute('select * from stock_application_details where stock_application_no=%s'  % session['barcode'] )
        new_data1=cur_new.fetchone()
        cur_old.execute('SELECT * FROM normality_sell_stocks_change_detail WHERE item_code="%s" and  nomal_change_id IN (SELECT id FROM normality_sell_stocks_change_log WHERE apply_no=%s ) ORDER BY id DESC'  %  (new_data1['barcode'],session['barcode']))
        old_data1=cur_old.fetchone()
        old_data1.pop('vendor_name')
        old_data1.pop('vendor_code')
        cur_old.execute('select * from normality_sell_goods where flagship_id=%s and goods_barcodes="%s"'  % (old_data1['flagship_id'],old_data1['item_code']))
        ji_data1=cur_old.fetchone()
        ji_data1.pop('vendor_name')
        ji_data1.pop('vendor_code')
        cur_old.execute('select * from normality_sell_stocks_change_log where apply_no=%s'  %  session['barcode'])
        s = cur_old.fetchone()
        ji1_data1={}
        ji1_data1['vendor_name']=s['vendor_name']
        ji1_data1['vendor_code'] = s['vendor_code']
        ji1_data1['apply_no'] = s['apply_no']
        cur_old.execute('select * from vendor_shop_schedule where shop_code=%s AND warehouse="%s"'  %  (old_data1['flagship_id'],old_data1['sell_area']))
        s = cur_old.fetchone()
        ji1_data1['schedule_id'] = s['schedule_id']
        cur_old.execute('SELECT * FROM purchase_agreement_goods  WHERE barcode="%s" limit 1'   %  new_data1['barcode'])
        s = cur_old.fetchone()
        ji1_data1['v_sku_id'] = s['v_sku_id']
        if new_data1==None  or  old_data1==None  or ji_data1==None :
            pass
        else:
          for i in k.data1:
            if i[0].strip()  in  new_data1.keys():
                i.insert(1, new_data1[i[0].strip() ])
            if i[2].split('*')[0].strip()  in  old_data1.keys():
                  i.insert(3, old_data1[i[2].strip() ])
            elif i[2].strip()  in  ji_data1.keys():
                i.insert(3,  ji_data1[i[2].strip()])
            elif i[2].strip()  in  ji1_data1.keys():
                print 111111111111111777777777777777777
                print i[2]
                i.insert(3,  ji1_data1[i[2].strip()])
            else:
                i.insert(3, 'no data')
    else:
        for i in k.data1:
                i.insert(1, 'no data')
                i.insert(3, 'no data')
    if 'barcode'   in session.keys():
        cur_new.execute('select * from stock_product_status where stock_application_no=%s'  % session['barcode'] )
        new_data2=cur_new.fetchone()
        print 12334524524524524525
        print  new_data2['barcode'],session['barcode']
        cur_old.execute('SELECT * FROM visAdmin.normality_sell_goods WHERE goods_barcodes="%s" and nomal_change_id IN (SELECT id FROM visAdmin.normality_sell_stocks_change_log WHERE apply_no=%s) ORDER BY id DESC'  %  (new_data2['barcode'],session['barcode']))
        old_data2=cur_old.fetchone()
        print 66666666666666666666
        if new_data2==None  or  old_data2==None  :
            pass
        else:
          for i in k.data2:
            if i[0].strip()  in  new_data2.keys():
                i.insert(1, new_data2[i[0].strip() ])
            if i[2].split('*')[0].strip()  in  old_data2.keys():
                  i.insert(3, old_data2[i[2].strip() ])
            else:
                i.insert(3, 'no data')
    else:
        for i in k.data2:
                i.insert(1, 'no data')
                i.insert(3, 'no data')
    return render_template('/simple_page/tabs_kaifa.html',b=k.table0,value=k.data0,b1=k.table1,value1=k.data1,b2=k.table2,value2=k.data2)
@app.route('/yansql', methods=['GET','POST'])
def  yan_sql():
    print request.form
    session['barcode']= request.form['barcode']
    print session['barcode']
    return jsonify(a='1')
#测试返回测试前段接口信息(不是自动打开的页面，是手动打开的页面)
from lenove_jie_kou.ceshi_no import *
@app.route('/signal_run', methods=[ 'POST','GET'])
@ceshi_no
def signal_run():
    pass

#接收接口测试返回过来的批量接口数据，并存入数据库中
from lenove_jie_kou.run_jiekou import *
@app.route('/jie_kou_result', methods=[ 'POST','GET'])
@jiekou_result
def jiek_result():
    pass
#所有接口信息列表展示
from lenove_jie_kou.jiekou_list import jiekou_list_show
@app.route('/jiekou_list', methods=[ 'POST','GET'])
@jiekou_list_show
def jiekou_list_show():
     pass
#根据运行按钮批量运行脚本并弹出结果页面
from lenove_jie_kou.jiekou_list import jiekou_result_run
@app.route('/simple_jie_kou_run', methods=[ 'POST','GET'])
@jiekou_result_run
def jiekou_list_showeeaa():
     pass
#get请求为打开修改配置文件弹出框，获取第一个选中元素的class值，返回对应配置目录下的配置文件值
#post请求为获取要更新的配置，在相应目录下更新。
from lenove_jie_kou.change_config import change_config
@app.route('/read_configparse', methods=[ 'POST','GET'])
@change_config
def jiekou_list_showeeaa():
     pass
from lenove_jie_kou.jiekou_list import *
@app.route('/jiaobenshuru', methods=['POST'])
@jiaobenshuru
def jiaoben_shuru():
   pass
#跳转到试试调试页面
@app.route('/shishitiaoshi', methods=['GET','POST'])
@shishitiaoshi
def shishitiaoshi():
    pass
#调试url入库
@app.route('/jiekou_mulu', methods=['GET','POST'])
@url_insert
def jiekou_mulu():
  pass

#前端页面输入接口list的目录
@app.route('/uplate_jiekou_list', methods=['GET','POST'])
def uplate_jiekou_listaadd():
    ip = request.remote_addr
    db = sqlite3.connect(current_app.config.get('JIE_KOU'))
    cu = db.cursor()
    if len(cu.execute('select * from jiekou_mulu where ip=? and statu=?',
                      (request.remote_addr, u'批量')).fetchall()) > 0:
        cu.execute('update jiekou_mulu set mulu=?,update_time=? where ip=? and statu=?',
                   (request.form['mulu'], str(time.time()), request.remote_addr,u'批量'))
    else:
        cu.executemany('INSERT INTO jiekou_mulu VALUES (null,?,?,?,?)',
                       [(u'批量', request.form['mulu'], request.remote_addr, str(time.time()))])
    db.commit()
    db.close()
    if ip == "127.0.0.1":
        ip = '192.168.137.1'
    if request.method=="POST":
        mulu=request.form['mulu']
    else:
        if session.has_key('gen_mulu'):
            mulu=session['gen_mulu']
        else:
            return render_template('/hualala/pages/jiekou_list.html', yewu_name='',
                                   select_huanjing='', huanjing='',
                                   all_mulu='')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 8065))
    s.send('jiekou_mulu')
    b=s.recv(1024)
    if b == 'please':
        s.send(mulu)
        data = json.loads(s.recv(1024))
    session['gen_mulu']=mulu
    return render_template('/hualala/pages/jiekou_list.html', yewu_name=data['yewu_name'],select_huanjing=data['select_huanjing'], huanjing=data['huanjing'],all_mulu=session['gen_mulu'] )

#调试url入库
@app.route('/get_mulu', methods=['GET','POST'])
@get_mulua
def get_mulua():
  pass

#批量运行接口
@app.route('/piliang_run', methods=['GET','POST'])
@piliang_run
def piliang_run():
  pass
#获取后端发过来的本地批量运行的结果并存入数据库中
@app.route('/piliang_run_result', methods=['GET','POST'])
@piliang_run_resulttt
def piliang_run_result():
  pass



#获取接口运行结果
@app.route('/jie_kou_result', methods=['GET','POST'])
def jie_kou_result():
  return jsonify(a="1")

#从数据库中拉取数据，返回批量测试结果
from lenove_jie_kou.run_jiekou import *
@app.route('/jie_kou', methods=[ 'POST','GET'])
@piliangjiekou_result
def run_jiekou():
    pass


#接口git 页面返回
@app.route('/jiekou_page', methods=['GET', 'POST'])
@jiekou_piliang
def jiekou_page():
   pass
'''
接口路由结束
 '''
#项目首页，如果是post请求则是输入进来git，自动从相关目录下获取git文件地址
@app.route('/first_page', methods=['GET', 'POST'])
def first_page_exe():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    name = cu.execute(
        'select name from user where ip="%s" order by time desc limit 0,1' % request.remote_addr).fetchall()
    if len(name)==0:
        return redirect(url_for('login_new'))
    else:
        name=name[0][0]
    if request.method == 'GET':
        git_detail = [list(i) for i in cu.execute('select * from git_detail  ').fetchall()]
        for i in git_detail:
            i[3] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(i[3])))
        email_detail =[ i[0]  for i in cu.execute('select address from email_address where user="%s"'  % (name)).fetchall()]
        fajianren = [i[0] for i in db.execute('select email_user from fajianren where name="%s"' % name).fetchall()]
        dingshi_detail = [[i[1],i[2],i[4],i[6]] for i in cu.execute('select * from dingshi_run where name="%s" order by update_time desc ' % (name)).fetchall()]
        jobs= [i[0] for i in db.execute('select job_name from jekins where name="%s"' % name).fetchall()]
        for k,i in enumerate(dingshi_detail):
            i.insert(0,i[0])
            i[1]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i[0])))
            if i[-2].strip()=='0':
                i[-2]=u'ready'
            elif i[-2].strip()=='1':
                i[-2]=u'running'
            elif i[-2].strip()=='2':
                i[-2]=u'over'
            print i
        time_date = time.strftime('%Y-%m-%d ', time.localtime(time.time()))
        server_detail =[ i[1]  for i in cu.execute('select * from all_server where statu="1"').fetchall()]
        db.close()
        return render_template('/hualala/pages/index.html', git_detail=git_detail,email_detail=email_detail,time_date=time_date,dingshi_detail=dingshi_detail,fajianren=fajianren,jobs=jobs,server_detail=server_detail)
    else:
        git_url = request.form['git'].strip()
        git_beizhu = request.form['beizu'].strip()
        git_branch = request.form['branch'].strip()
        if git_url.strip() != '' and git_beizhu.strip() != '':
            cu.executemany('INSERT INTO git_detail VALUES (?,?,?,?,?,?)',
                           [(git_url, git_beizhu, name, str(time.time()), '',git_branch)])
            db.commit()
            db.close()
        return jsonify(a='1')
#登陆页面
@app.route('/login', methods=['GET', 'POST'])
def login_new():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    if request.method == 'GET':
        db.close()
        return render_template('/hualala/login.html')
    else:
        ip = request.remote_addr
        name = request.form['name']
        passs = request.form['password']
        user_check = cu.execute('select * from user where name="%s" and pass="%s" ' % (name, passs)).fetchall()
        if len(user_check) != 0:
            # cu.executemany('UPDATE user SET ip="null" WHERE ip=?', [(ip)])
            db.commit()
            cu.executemany('update  user  set time=? ,ip=? where name=?', [(time.time(), ip, name)])
            db.commit()
            db.close()
            return redirect(url_for('first_page_exe'))
        else:
            db.close()
            return render_template('/hualala/login.html')
#用户管里页面
from hualala.user import  *
@app.route('/user_manage', methods=['GET', 'POST'])
@user
def user_manage():
     pass
#server管里页面
@app.route('/server_manage', methods=['GET', 'POST'])
@server
def server_manage():
     pass
#server启动停止
@app.route('/change_server', methods=['GET', 'POST'])
def change_server():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    if request.form['statu']=='true':
        statu='0'
    else:
        statu='1'
    cu.executemany('update   all_server set statu=? where id=?',[(statu,int(request.form['change_id']))])
    db.commit()
    db.close()
    return jsonify(a=1)
#server增加
@app.route('/add_server', methods=['GET', 'POST'])
def add_server():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    if request.form['ip'].strip()==''or request.form['duankou'].strip()=='':
        return jsonify(a=u"输入不能为空")
    elif len(cu.execute('select * from all_server where ip="%s"' %(request.form['ip'])).fetchall())>0:
        return jsonify(a=u"server ip 已经存在")
    cu.executemany('INSERT INTO  all_server values (null,?,?,?,?)', [(request.form['ip'],request.form['duankou'],'0','0')])
    db.commit()
    db.close()
    return jsonify(a=1)
#脚本运行
from hualala.run import  *
@app.route('/run_hualala', methods=['GET', 'POST'])
@run_hualala
def run_hual():
     pass
#运行检查
from hualala.run import  *
@app.route('/run_charge', methods=['GET', 'POST'])
@run_charge
def run_hual():
     pass
@app.route('/delete_ben',methods=['GET', 'POST'])
def delete_ben():
    if request.form['statu']=='url':
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
    else:
        db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu = db.cursor()
    ip = request.remote_addr
    name=request.form['name'].strip()
    branch=request.form['branch'].strip()
    git=request.form['git'].strip()
    cu.execute('delete from git_detail  where  name="%s"  and submit= "%s"  and  branch= "%s"  ' % (git,name,branch)).fetchall()
    db.commit()
    db.close()
    return jsonify(statu='success')
from hualala.add_email import  *
@app.route('/add_email',methods=['GET', 'POST'])
@add_email
def add_email():
    pass
@app.route('/emali_list_all',methods=['GET', 'POST'])
@show_email
def emali_list():
    pass
@app.route('/delete_email',methods=['GET', 'POST'])
@delete_email
def emali_list():
    pass
@app.route('/send_emali',methods=['GET', 'POST'])
@send_emali
def send_emali():
    pass
@app.route('/add_file_detail',methods=['GET', 'POST'])
@add_file_detail
def add_file_detail():
    pass
@app.route('/dingshi_result/<id>',methods=['GET', 'POST'])
def dingshi_result(id):
    # 查看定时运行的结果文件
            db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
            cu = db.cursor()
            url_detail='http://'+socket.gethostbyname(socket.gethostname())+':5021'+ url_for('dingshi_result',id=id)
            if str(id).strip()=='shishi':
                    #name = cu.execute('select name from user where ip="%s" order  by time desc limit 0,1 ' % request.remote_addr).fetchall()[0][0]
                    z = cu.execute('select run_result from dingshi_run where id=?', (id).fetchall()[0][0])
                    timee = cu.execute('select update_time,last_run_time from dingshi_run where id=?',
                                      (id)).fetchall()[0]
                    print timee
            else:
                z = cu.execute('select run_result from dingshi_run where id=?', (id,)).fetchall()[0][0]
                timee = cu.execute('select update_time,last_run_time from dingshi_run where  id=?', (id,)).fetchall()[0]
                z = json.loads(z)
            job = json.loads(cu.execute('select job from dingshi_run where id=?', (id,)).fetchall()[0][0])
            if 'name' in job.keys() and 'no select' !=job['name'].strip():
               job_r=job['name']+':'+job['result']
            else:
                job_r='null'
            run_taken=float(job['end_time'])
            if run_taken>60:
                run_time_detail=str(int(run_taken)/60)+u'分'+str(int(run_taken)%60)+u'秒'
            else:
                run_time_detail=str(int(run_taken))+u'秒'
            total=[0,0,0,0]
            timeArray = time.localtime(float(timee[0]))
            otherStyleTime = time.strftime("%H:%M:%S", timeArray)
            timee=list(timee)
            if timee[1].strip()=='':
                timee[1] = time.strftime('%Y:%m:%d', timeArray)
            timee=timee[1]+'   '+otherStyleTime
            for k in z:
                total[0]+=z[k]['count']
                total[1] += z[k]['Pass']
                total[2] += z[k]['fail']
                total[3] += z[k]['error']

            db.close()
            return render_template('/hualala/pages/test_result.html', time=str(time.time()), z=z,total=total,timee=timee,job=job_r,taken=run_time_detail,url_detail=url_detail)
@app.route('/open_dingshi_detail',methods=['GET', 'POST'])
@open_dingshi_detail
def open_dingshi_detail():
    pass
#设置发件人
@app.route('/add_fajianren',methods=['GET', 'POST'])
@add_fajianren
def add_fajianren():
    pass
#显示 发件人
@app.route('/show_fajianren',methods=['GET'])
@show_fajianren
def show_fajianren():
    pass
#删除发件人
@app.route('/delete_fajianren',methods=['GET'])
@delete_fajianren
def delete_fajianren():
    pass
#设置jekins
@app.route('/add_jekins',methods=['GET', 'POST'])
@add_jekins
def add_fajianren():
    pass
#jekins_list 列表
@app.route('/jekins_list',methods=['GET', 'POST'])
@jekins_list
def jekins_list():
    pass
#jekins_list删除
@app.route('/jekins_delete',methods=['GET', 'POST'])
@jekins_delete
def jekins_delete():
    pass
#suite_list删除
@app.route('/suite_delete',methods=['GET', 'POST'])
@suite_delete
def suite_delete():
    pass
#suite_list删除
@app.route('/xiaomin',methods=['GET', 'POST'])
def xiaomin():
   a=222
   return jsonify(statu='success')
#打开second 页面
@app.route('/second_page',methods=['GET', 'POST'])
def second():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    name = cu.execute(
        'select name from user where ip="%s" order by time desc limit 0,1' % request.remote_addr).fetchall()
    if len(name) == 0:
        return redirect(url_for('login_new'))
    else:
        name = name[0][0]
    data = cu.execute('select * from locust_file order by id desc').fetchall()
    db.close()
    return render_template('/hualala/pages/second_page.html',data=data)
#上传脚本文件
from hualala.locust_fiel import upload_fil
@app.route('/upload_file',methods=['GET', 'POST'])
@upload_fil
def upload_file():
    pass
#上传脚本文件同时更新文件表格信息
from hualala.locust_fiel import upload_fil_beizu
@app.route('/upload_fil_beizu',methods=['GET', 'POST'])
@upload_fil_beizu
def upload_file():
    pass