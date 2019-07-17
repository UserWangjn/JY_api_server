# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\jieyuelianhe\old_all_server\THREAD_BEIFEN\THREAD_fuben\jie_kou_test\pi_run\pi_run.py
# Compiled at: 2019-05-05 14:32:14
__author__ = 'SUNZHEN519'
import sys, os, re
sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))
from selenium import webdriver
import time as timee, traceback, chardet, unittest, demjson, urllib, random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import unittest, xlrd, ConfigParser, json, urllib2, os, logging
from excel_data import *
import hashlib
from just_run.save_global_data import set_global_data
from json_pi_pei.request_result_flask import *
from json_pi_pei.before_after_sql import before_after_sql
from json_pi_pei.json_pi_pei import *
from json_pi_pei.request_run import *
from sing_data.haofang_server import haofang_login
from sing_data.huasheng import hs_login
from just_run.change_request_before import change_request_before
from just_run.just_run import just_run
from assert_run.assert_run import *

class pi_run(object):

    def __init__(self, path, timee, ip, server_ip, all_bianliang, run_id, git_base_name):
        self.git_base_name = git_base_name
        self.all_bianliang = all_bianliang
        self.path = os.path.normpath(path)
        self.run_time = timee
        self.server_ip = server_ip
        excel_name = os.path.basename(self.path)
        for dir, b, file in os.walk(self.path):
            for z in file:
                if excel_name in z:
                    self.excel_path = os.path.join(self.path, z)
                elif 'json' == z.split('.')[0]:
                    self.json_path = os.path.join(self.path, z)
                elif 'configparse' == z.split('.')[0]:
                    self.config_path = ConfigParser.SafeConfigParser()
                    self.config_path.read(os.path.join(self.path, z))
                    self.config_path.set('config', 'mulu', self.path)
                    db_config_path = os.path.join(os.path.dirname(self.path), 'db.txt')
                    content = open(db_config_path).read()
                    content = re.sub('\\xfe\\xff', '', content)
                    content = re.sub('\\xff\\xfe', '', content)
                    content = re.sub('\\xef\\xbb\\xbf', '', content)
                    open(db_config_path, 'w').write(content)
                    db_config = ConfigParser.ConfigParser()
                    db_config.read(db_config_path)
                    db_sql = {}
                    if os.path.isfile(os.path.join(os.path.dirname(self.path), 'db.txt')) and self.config_path.get('sign', 'sign_type').strip() in ('zhixin', ):
                        for i in db_config.sections():
                            self.config_path.add_section(i)
                            [ self.config_path.set(i, k, db_config.get(i, k)) for k in db_config.options(i) ]

                    if os.path.isfile(os.path.join(os.path.dirname(self.path), 'db.txt')):
                        if 'sql' in db_config.sections():
                            for k in db_config.options('sql'):
                                db_sql[k] = db_config.get('sql', k)

                    if os.path.isfile(os.path.join(os.path.dirname(self.path), 'config.txt')):
                        public_config_path = os.path.join(os.path.dirname(self.path), 'config.txt')
                        private_config_path = os.path.join(self.path, 'configparse.txt')
                        private_config = ConfigParser.ConfigParser()
                        public_config = ConfigParser.ConfigParser()
                        public_config.read(public_config_path)
                        private_config.read(private_config_path)
                        if os.path.isfile(public_config_path):
                            if 'sign' in public_config.sections():
                                if 'run_interval' in self.config_path.options('sign'):
                                    self.time_interval = float(self.config_path.get('sign', 'run_interval'))
                                else:
                                    if 'run_interval' in public_config.options('sign'):
                                        self.time_interval = float(public_config.get('sign', 'run_interval'))
                                    else:
                                        self.time_interval = 0
                                self.config_path.set('sign', 'run_interval', str(self.time_interval))
                            if self.config_path.get('sign', 'sign_type').strip() == 'web':
                                if 'login' not in self.config_path.sections():
                                    self.config_path.add_section('login')
                                if 'login' in private_config.sections() and all(k in private_config.options('login') for k in public_config.options('login')):
                                    [ public_config.set('login', z, private_config.get('login', z)) for z in private_config.options('login') ]
                                [ self.config_path.set('login', z, public_config.get('login', z)) for z in public_config.options('login')
                                ]
                                headers_dict = web_token(self.config_path)
                                self.config_path.set('login', 'headers_dict', json.dumps(headers_dict))
                                self.config_path.add_section('login_value')
                                hash = hashlib.md5()
                                code = self.config_path.get('login', 'url').strip() + self.config_path.get('login', 'name').strip() + self.config_path.get('login', 'password').strip()
                                hash.update(code)
                                self.config_path.set('login_value', str(hash.hexdigest()), json.dumps(headers_dict))
                                head_key = private_config.get('config', 'head_key').split('.')
                                head_value = private_config.get('config', 'head_value').split('.')[:len(head_key)]
                                header_older = json.dumps(dict(zip(head_key, head_value)))
                                self.config_path.set('login', 'headers_old', header_older)
                            else:
                                if self.config_path.get('sign', 'sign_type').strip() in ('app',
                                                                                         'xiang_qian'):
                                    header_dict = {'Content-Type': 'application/json'}
                                    self.config_path.add_section('app_head')
                                    self.config_path.set('app_head', 'app_head', json.dumps(header_dict))
                                else:
                                    if self.config_path.get('sign', 'sign_type').strip() == 'jy_appServer':
                                        if 'sign_url' in public_config.sections() and 'sign_url' not in self.config_path.sections():
                                            self.config_path.add_section('sign_url')
                                            self.config_path.set('sign_url', 'encode_url', public_config.get('sign_url', 'encode_url'))
                                            self.config_path.set('sign_url', 'decode_url', public_config.get('sign_url', 'decode_url'))
                                    else:
                                        if self.config_path.get('sign', 'sign_type').strip() == 'zhixin':
                                            if 'login' not in self.config_path.sections():
                                                self.config_path.add_section('login')
                                            self.config_path.set('login', 'url', public_config.get('login', 'url'))
                                            self.config_path.set('login', 'name', public_config.get('login', 'name'))
                                            self.config_path.set('login', 'password', public_config.get('login', 'password'))
                                            self.config_path.set('login', 'secret', public_config.get('login', 'secret'))
                                            if 'login_name' in db_config.options('data'):
                                                self.config_path.set('login', 'name', db_config.get('data', 'login_name'))
                                            if 'login_password' in db_config.options('data'):
                                                self.config_path.set('login', 'password', db_config.get('data', 'login_password'))
                                            if 'login_secret' in db_config.options('data'):
                                                self.config_path.set('login', 'password', db_config.get('data', 'login_secret'))
                                            if 'login_token' in self.all_bianliang.keys() and 'login' in self.config_path.sections():
                                                if self.config_path.get('login', 'name') == self.all_bianliang['name'] and self.config_path.get('login', 'password') == self.all_bianliang['password']:
                                                    self.config_path.set('login', 'token', self.all_bianliang['login_token'])
                                            header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko', 
                                               'Content-Type': 'application/json'}
                                            self.config_path.add_section('app_head')
                                            self.config_path.set('app_head', 'app_head', json.dumps(header_dict))
                                            if 'token' not in self.config_path.options('login'):
                                                token = zhixin_login(self.config_path.get('login', 'name').strip(), self.config_path.get('login', 'password').strip(), self.config_path.get('login', 'url').strip(), self.config_path.get('login', 'secret').strip())
                                                self.config_path.set('login', 'token', token)
                                            else:
                                                token = self.config_path.get('login', 'token')
                                            self.config_path.add_section('data')
                                            self.config_path.set('data', 'token', token)
                                            save_data_normal(self.path, 'data', 'token', token)
                                        else:
                                            if self.config_path.get('sign', 'sign_type').strip() == 'Backstage_web':
                                                if 'login' not in self.config_path.sections():
                                                    self.config_path.add_section('login')
                                                self.config_path.set('login', 'url', public_config.get('login', 'url'))
                                                self.config_path.set('login', 'name', public_config.get('login', 'name'))
                                                self.config_path.set('login', 'password', public_config.get('login', 'password'))
                                                if 'login_token' in self.all_bianliang.keys() and 'login' in self.config_path.sections():
                                                    if self.config_path.get('login', 'name') == self.all_bianliang['name'] and self.config_path.get('login', 'password') == self.all_bianliang['password']:
                                                        self.config_path.set('login', 'token', self.all_bianliang['login_token'])
                                                header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko', 
                                                   'Content-Type': 'application/json'}
                                                self.config_path.add_section('app_head')
                                                self.config_path.set('app_head', 'app_head', json.dumps(header_dict))
                                                if 'token' not in self.config_path.options('login'):
                                                    token = houtai_jiami(self.config_path.get('login', 'name').strip(), self.config_path.get('login', 'password').strip(), self.config_path.get('login', 'url').strip())
                                                    self.config_path.set('login', 'token', token)
                                                else:
                                                    token = self.config_path.get('login', 'token')
                                                save_data_normal(self.path, 'data', 'token', token)
                                            else:
                                                if self.config_path.get('sign', 'sign_type').strip() == 'haofang_server':
                                                    if 'login' not in self.config_path.sections():
                                                        self.config_path.add_section('login')
                                                    self.config_path.set('login', 'url', public_config.get('login', 'url'))
                                                    self.config_path.set('login', 'name', public_config.get('login', 'name'))
                                                    self.config_path.set('login', 'password', public_config.get('login', 'password'))
                                                    if 'haofang_headertoken' in self.all_bianliang.keys():
                                                        if self.config_path.get('login', 'name') == self.all_bianliang['name'] and self.config_path.get('login', 'password') == self.all_bianliang['password']:
                                                            self.config_path.set('login', 'haofang_headertoken', self.all_bianliang['haofang_headertoken'])
                                                        else:
                                                            self.all_bianliang['name'] = self.config_path.get('login', 'name')
                                                            self.all_bianliang['password'] = self.config_path.get('login', 'password')
                                                            haofang_headertoken = json.dumps(haofang_login(self.config_path.get('login', 'name').strip(), self.config_path.get('login', 'password').strip(), self.config_path.get('login', 'url').strip()))
                                                            self.all_bianliang['haofang_headertoken'] = haofang_headertoken
                                                            self.config_path.set('login', 'haofang_headertoken', self.all_bianliang['haofang_headertoken'])
                                                else:
                                                    if self.config_path.get('sign', 'sign_type').strip() == 'hkci':
                                                        if 'login' not in self.config_path.sections():
                                                            self.config_path.add_section('login')
                                                        self.config_path.set('login', 'login_url', public_config.get('login', 'login_url'))
                                                        self.config_path.set('login', 'server_host', public_config.get('login', 'server_host'))
                                                        self.config_path.set('login', 'phone', public_config.get('login', 'phone'))
                                                        self.config_path.set('login', 'ling_pai', public_config.get('login', 'ling_pai'))
                                                        self.config_path.set('login', 'dian_pu', public_config.get('login', 'dian_pu'))
                                                        if 'huasheng_headertoken' in self.all_bianliang.keys():
                                                            if self.config_path.get('login', 'phone') == self.all_bianliang['phone'] and self.config_path.get('login', 'ling_pai') == self.all_bianliang['ling_pai'] and self.config_path.get('login', 'dian_pu') == self.all_bianliang['dian_pu']:
                                                                self.config_path.set('login', 'huasheng_headertoken', self.all_bianliang['huasheng_headertoken'])
                                                        else:
                                                            self.all_bianliang['phone'] = self.config_path.get('login', 'phone')
                                                            self.all_bianliang['ling_pai'] = self.config_path.get('login', 'ling_pai')
                                                            self.all_bianliang['dian_pu'] = self.config_path.get('login', 'dian_pu')
                                                            get_mendian_detail_url = self.config_path.get('login', 'server_host') + '/hk-peanut-car/api/place/getLoginPlaceInfo'
                                                            db_detail = [db_config.get('db_mysql_login', 'host'), db_config.get('db_mysql_login', 'port'),
                                                             db_config.get('db_mysql_login', 'user'), db_config.get('db_mysql_login', 'password'), db_config.get('db_mysql_login', 'db')]
                                                            huasheng_headertoken = hs_login(self.config_path.get('login', 'server_host'), db_detail, self.config_path.get('login', 'login_url'), self.config_path.get('login', 'phone'), self.config_path.get('login', 'dian_pu'), self.config_path.get('login', 'ling_pai'))
                                                            self.all_bianliang['huasheng_headertoken'] = huasheng_headertoken
                                                            self.config_path.set('login', 'huasheng_headertoken', self.all_bianliang['huasheng_headertoken'])
                                                        save_data_normal(self.path, 'data', 'huasheng_headertoken', self.all_bianliang['huasheng_headertoken'])
                            if public_config.get('url', 'public_url').strip() != '':
                                url = self.config_path.get('config', 'private_url')
                                self.config_path.set('config', 'public_url', public_config.get('url', 'public_url').strip())
                                self.config_path.set('config', 'url', public_config.get('url', 'public_url').strip() + url.strip())

        if os.path.isfile(os.path.join(os.path.dirname(self.path), 'db.txt')) and self.config_path.get('sign', 'sign_type').strip() != 'zhixin':
            db_config_path = os.path.join(os.path.dirname(self.path), 'db.txt')
            db_config = ConfigParser.ConfigParser()
            db_config.read(db_config_path)
            for i in db_config.sections():
                self.config_path.add_section(i)
                for k in db_config.options(i):
                    try:
                        self.config_path.set(i, k, db_config.get(i, k))
                    except:
                        pass

        self.data = xlrd.open_workbook(self.excel_path)
        self.table = self.data.sheets()[0]
        self.key = self.table.row_values(0)
        self.data = []
        _statu = 0
        for k, i in enumerate(self.key):
            if i.strip() == 'id':
                if _statu == 0:
                    _statu = 1
                else:
                    self.key[k] = 'id_canshu'
            if type(i) == float:
                self.key[k] = int(i)

        self.data = [ dict(zip(self.key, self.table.row_values(i))) for i in range(1, self.table.nrows) ]
        before_request = change_request_before(self.all_bianliang)
        self.all_result = {}
        self.flask_result = {}
        self.config_path.set('config', 'mulu_path', self.path)
        for k, i in enumerate(self.data):
            if len(db_sql) != 0:
                for sql_key, sql_value in db_sql.iteritems():
                    self.config_path.set('sql', sql_key, sql_value)

            if str(i['id']).strip() == '' or str(i['Comment']) == '' or '#' in str(i['id']):
                pass
            self.result_key = str(i['result']) + 'jo.in' + str(i['id']) + 'jo.in' + str(i['Comment'])
            case_assert, case_id, case_name = i['result'], i['id'], i['Comment']
            case_assert = copy.deepcopy(i['result'])
            try:
                if str(i['id']) == '' or '#' in str(i['id']):
                    continue
                self.all_bianliang['before_case_detail'][self.path][int(i['id'])]
                if len(self.all_bianliang['before_case_detail'][self.path][int(i['id'])]) == 0:
                    if 'head_data' in self.key and i['head_data'].strip() != '':
                        request_header = change_data_db(self.config_path, i['head_data'], i).data
                        if 'head_data' not in self.config_path.sections():
                            self.config_path.add_section('head_data')
                        self.config_path.set('head_data', 'head_data', request_header)
                    if open(self.json_path).read().decode('GB2312').strip() != '':
                        j = json.loads(open(self.json_path).read().decode('GB2312'))
                    else:
                        j = ''
                    try:
                        print '开始调用,id值为%s,路径为%s' % (str(self.data[k]['id']), self.excel_path.decode('gb2312'))
                    except:
                        print '开始调用,id值为%s,路径为%s' % (str(self.data[k]['id']), self.excel_path)

                    if 'global_data' in self.key and i['global_data'].strip() != '':
                        set_global_data().set_global_data(i, self.config_path, self.path, all_bianliang)
                    if 'before_sql' in self.key and i['before_sql'] != '':
                        before_after_sql(i['before_sql'], db_config)
                        i.pop('before_sql')
                    after_sql = ''
                    if 'after_sql' in self.key and i['after_sql'] != '':
                        after_sql = i.pop('after_sql')
                    if 'before_request' in self.key:
                        i['before_request'] = i['before_request'].strip()
                        self.data[k] = before_request.use(i, self.path, self.config_path)
                        if type(self.data[k]) in [str, unicode]:
                            self.data[k] = json.loads(self.data[k])
                    if 'before_request' in self.key and i['before_request'].strip() != '' and 'err_detail' in self.data[k].keys():
                        self.all_result[self.result_key + 'jo.in' + json.dumps(json.dumps({'before_request_error': str(self.data[k]['err_detail'])}))] = self.data[k]
                        continue
                    self.s = excel_data_exe()
                    for key, value in i.iteritems():
                        if key == 'contactList':
                            pass
                        try:
                            if str(value)[0] != '0' and int(value) == float(value):
                                i[key] = str(int(value))
                        except:
                            pass
                        else:
                            if type(value) not in [float, int, long] and value != None and '##' in value:
                                self.s = excel_data_exe()
                                self.data[k][key] = self.s.han_shu(value)
                                i[key] = self.s.han_shu(value)
                            elif type(value) == list:
                                self.s = excel_data_exe()
                                self.data[k][key] = self.s.han_shu(value)
                                i[key] = self.s.han_shu(value)

                    self.url = ''
                    change_json_data(j, i)
                    if 'id_data' in i.keys():
                        i['id'] = i.pop('id_data')
                    if 'result_data' in i.keys():
                        i['result'] = i.pop('result_data')
                    if 'url' in i.keys() and i['url'].strip() != '':
                        if os.path.isfile(os.path.join(os.path.dirname(self.path), 'config.txt')) and public_config.get('url', 'public_url').strip() != '':
                            url = self.config_path.get('config', 'url')
                            i['url'] = public_config.get('url', 'public_url').strip() + i['url']
                        self.url = str(i['url'])
                    if 'json' in i.keys() and i['json'] != '':
                        self.req = json.dumps(json.loads(i['json']))
                    else:
                        self.req = i
                    if 'id_canshu' in self.req.keys():
                        self.id_beifen = self.req.pop('id')
                        self.req['id'] = self.req.pop('id_canshu')
                    self.req = creat_json(copy.deepcopy(j), self.req)
                    self.req = json.loads(change_data_db(self.config_path, self.req).data)
                    port = request_run(j, self.config_path, self.path)
                    self.result_key = str(i['result']) + 'jo.in' + str(i.pop('id')) + 'jo.in' + str(i['Comment'])
                    if self.url != '':
                        if self.config_path.get('config', 'method') == 'post':
                            try:
                                self.respons = port.post(self.req, self.config_path, self.url)['respons']
                                if self.respons != '':
                                    self.respons = json.loads(self.respons)
                            except:
                                self.respons = {'result': port.post(self.req, self.config_path, self.url)['respons']}

                        elif self.config_path.get('config', 'method') == 'get':
                            try:
                                self.respons = port.get(self.req, self.config_path, self.url)['respons']
                                if self.respons != '':
                                    self.respons = json.loads(self.respons)
                            except:
                                self.respons = {'result': port.get(self.req, self.config_path, self.url)['respons']}

                        elif self.config_path.get('config', 'method') == 'delete':
                            try:
                                self.respons = port.delete(self.req, self.config_path, self.url)['respons']
                                if self.respons != '':
                                    self.respons = json.loads(self.respons)
                            except:
                                self.respons = {'result': port.delete(self.req, self.config_path, self.url)['respons']}

                    else:
                        if self.config_path.get('config', 'method') == 'post':
                            self.respons = port.post(self.req, self.config_path)['respons']
                            if self.respons != '':
                                try:
                                    self.respons = json.loads(self.respons)
                                except:
                                    self.respons = {'result': port.get(self.req, self.config_path)['respons']}

                        else:
                            if self.config_path.get('config', 'method') == 'get':
                                try:
                                    self.respons = port.get(self.req, self.config_path)['respons']
                                    if self.respons != '':
                                        self.respons = json.loads(self.respons)
                                except:
                                    self.respons = {'result': port.get(self.req, self.config_path)['respons']}

                            else:
                                if self.config_path.get('config', 'method') == 'delete':
                                    try:
                                        self.respons = port.delete(self.req, self.config_path)['respons']
                                        if self.respons != '':
                                            self.respons = json.loads(self.respons)
                                    except:
                                        self.respons = {'接口返回': port.delete(self.req, self.config_path)['respons']}

                    if after_sql != '':
                        sql_statu = before_after_sql(after_sql, db_config)
                        if sql_statu['statu'] != 'success':
                            self.respons = sql_statu
                    if 'save_data' in i.keys():
                        save_data_config(i, self.path, self.config_path, self.respons)
                    if type(self.req) != dict:
                        self.req = json.loads(self.req)
                else:
                    self.req = self.all_bianliang['before_case_detail'][self.path][int(i['id'])]['request']
                    self.respons = self.all_bianliang['before_case_detail'][self.path][int(i['id'])]['result']
                self.assert_run = assert_run(self.config_path)
                if case_assert != '':
                    result_data = json.loads(change_data_db(self.config_path, case_assert, i).data)
                else:
                    result_data = ''
                case_assert = result_data
                self.assert_result = self.assert_run.walk_find(case_assert, self.respons)
            except Exception as e:
                print traceback.format_exc()
                error_detail = list([ i for i in re.findall('.*File "(.*)", line (.*), in(.*)', traceback.format_exc()) if os.path.isfile(i[0]) ][(-1)])
                error_detail.append(traceback.format_exc().split('\n')[(-2)])
                print error_detail
                for k, i in enumerate(error_detail):
                    if chardet.detect(i)['encoding'] not in ('utf-8', 'ascii', None):
                        error_detail[k] = i.decode(chardet.detect(i)['encoding'])

                if chardet.detect(str(e))['encoding'] not in ('utf-8', 'ascii', None):
                    e = str(e).decode(chardet.detect(str(e))['encoding'])
                self.respons = {'错误位置': '目录' + error_detail[0] + ',第' + str(error_detail[1]) + '行，函数：' + error_detail[2], '错误信息': str(e), 
                   '错误原因': cuowu_reson(error_detail)}
            else:
                try:
                    self.req
                except AttributeError:
                    self.req = ''
                else:
                    try:
                        self.assert_result
                    except:
                        self.assert_result = False
                    else:
                        try:
                            self.url
                        except AttributeError:
                            self.url = ''
                        else:
                            if self.url != '':
                                self.flask_result[int(float(case_id))] = {'case_assert': case_assert, 'case_name': case_name, 'req': self.req, 'respons': self.respons, 'assert_result': self.assert_result, 
                                   'req_url': self.url}
                            else:
                                try:
                                    self.flask_result[int(float(case_id))] = {'case_assert': case_assert, 'case_name': case_name, 'req': self.req, 
                                       'respons': self.respons, 'assert_result': self.assert_result, 
                                       'req_url': self.config_path.get('config', 'url')}
                                except:
                                    pass

                            if self.config_path.get('sign', 'sign_type') == 'Backstage_web':
                                self.all_bianliang['login_token'] = self.config_path.get('login', 'token')
                                self.all_bianliang['name'] = self.config_path.get('login', 'name').strip()
                                self.all_bianliang['password'] = self.config_path.get('login', 'password').strip()
                                self.all_bianliang['url'] = self.config_path.get('login', 'url').strip()
                            self.all_result[self.result_key + 'jo.in' + json.dumps(self.req)] = self.respons

        self.flask_result = json.dumps(self.flask_result)
        request_flask(excel_name, self.flask_result, self.run_time, ip, self.server_ip, self.path, run_id, self.git_base_name)
        return


if __name__ == '__main__':
    z = pi_run('C:\\work\\lenove_jie_kou\\Interface_automation\\queryPriceDetail')
    make_html([z.suite.suite], 'C:\\work\\lenove_jie_kou\\Interface_automation\\lenovo_jie_kou')