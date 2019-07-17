# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\Users\sunzhen\Desktop\web flask\HGTP_socket3\app\jie_kou_test\json_pi_pei\excel_data.py
# Compiled at: 2019-04-23 14:14:06
__author__ = 'SUNZHEN519'
import sys, re, requests, cx_Oracle, json, datetime
from selenium import webdriver
import time, chardet, unittest, demjson, pymysql, urllib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import unittest, xlrd, json, urllib2, os, logging, random, string
from sing_data.sing_xiangqian import *

class excel_data_exe(object):

    def han_shu(self, data):
        try:
            exe_data = json.loads(data)
        except:
            exe_data = data
        else:
            if type(exe_data) == list:
                for k, i in enumerate(exe_data):
                    if type(i) == dict:
                        for z, u in i.iteritems():
                            if '##' in u:
                                self.b = 'self.a='
                                exec self.b + u.split('##')[1]
                                exe_data[k][z] = self.a

                return json.dumps(exe_data)
            if type(exe_data) == dict:
                for k, i in exe_data:
                    if '##' in i:
                        self.b = 'self.a='
                        exec self.b + i.split('##')[1]
                        exe_data[k] = self.a

            else:
                if 'RSA:' in exe_data.split('##')[1]:
                    de_str = exe_data.split('##')[1].split('RSA:')[(-1)]
                    s = AESCipher('abcdnnnnnn123456')
                    return s.encrypt(de_str)
                if exe_data.split('##')[1] != 'random.str:12':
                    self.b = 'self.a='
                    exec self.b + exe_data.split('##')[1]
                    return self.a
            return ('').join(random.sample(string.ascii_letters + string.digits, int(data.split('##')[1].split(':')[(-1)])))


class change_data_db(object):

    def __init__(self, config, data, *take_data):
        if len(take_data) > 0:
            self.take_data = take_data[0]
        self.config = config
        self.error_data = 0
        try:
            self.data = json.loads(data)
        except:
            self.data = data
        else:
            if type(self.data) == dict:
                for k in self.data.keys():
                    if 'Comment' == k.strip():
                        continue
                    if type(self.data[k]) in [list, dict]:
                        try:
                            self.data[k] = json.loads(self.data[k])
                        except:
                            pass

                    if type(self.data[k]) in [str, unicode]:
                        self.data[k] = self.change_data(self.data[k], take_data)
                    elif len(take_data) != 0:
                        change_data_db(self.config, self.data[k], take_data)
                    else:
                        change_data_db(self.config, self.data[k])

            else:
                if type(self.data) == list:
                    for k, i in enumerate(self.data):
                        if type(self.data[k]) in [list, dict]:
                            try:
                                self.data[k] = json.loads(self.data[k])
                            except:
                                pass

                        if type(self.data[k]) in [str, unicode]:
                            self.data[k] = self.change_data(i, take_data)
                        elif len(take_data) != 0:
                            change_data_db(self.config, i, take_data)
                        else:
                            change_data_db(self.config, i)

                else:
                    self.change_data(self.data, take_data)
            try:
                if self.data != '':
                    self.data = json.dumps(self.data)
            except:
                pass

    def change_data(self, simple_data, take_data):
        self.simple_data = simple_data
        if 'select' in str(self.simple_data):
            pass
        error_data = ''
        try:
            self.take_data = json.loads(take_data)
        except:
            self.take_data = take_data
        else:
            if type(simple_data) in [unicode, str]:
                jisuan = '(\\(.*?\\))'
                if len(re.findall(jisuan, self.simple_data, re.M)) == 0 or 'select' in self.simple_data:
                    pattern = '(\\[.*?\\]\\[.*?\\]\\[.*?\\])'
                    guid = re.findall(pattern, self.simple_data, re.M)
                    for k, i in enumerate(guid):
                        if '"' in i:
                            guid[k] = i.split('"')[1]

                    if len(guid) == 0:
                        pattern = '(\\[.*?\\]\\[.*?\\])'
                        guid = re.findall(pattern, self.simple_data, re.M)
                        type_guid_simple = 0
                    else:
                        type_re = '(\\[.*?\\])'
                        type_guid_simple = re.findall(type_re, self.simple_data, re.M)[(-1)][1:-1]
                    error_data = ''
                    if len(guid) > 0:
                        guit = [ i[1:-1].split('][') for i in guid ]
                        for k, i in enumerate(guit):
                            if 'db' in i[0]:
                                for chang_statu in self.config.sections():
                                    if '[' + chang_statu + ']' in self.config.get('sql', i[1]):
                                        self.config.set('sql', i[1], self.change_data(self.config.get('sql', i[1]), take_data))
                                        self.simple_data = simple_data
                                        break

                                if 'json' in i[1]:
                                    if self.config.get(i[0], 'type').strip() == 'oracle':
                                        db = cx_Oracle.connect(self.config.get(i[0], 'conn'))
                                    else:
                                        db = pymysql.connect(host=self.config.get(i[0], 'host'), port=int(self.config.get(i[0], 'port')), user=self.config.get(i[0], 'user'), password=self.config.get(i[0], 'password'), db=self.config.get(i[0], 'db'))
                                    cursor = db.cursor()
                                    if cursor.execute(self.config.get('sql', i[1])) > 0:
                                        data = cursor.fetchone()[0]
                                        if 'json' in i[1]:
                                            can_shu = i[1].split('_')[(-1)]
                                            try:
                                                data = json.loads(data)
                                            except:
                                                data = 'sql返回的参数不是json格式'
                                            else:
                                                data = sql_json(data, can_shu)

                                        self.simple_data = self.simple_data.replace(guid[k], str(data).strip())
                                    else:
                                        error_data = '获取数据库数据失败'
                                else:
                                    if self.config.get(i[0], 'type').strip() == 'oracle':
                                        try:
                                            db = cx_Oracle.connect(self.config.get(i[0], 'conn'))
                                        except:
                                            pass

                                    else:
                                        if self.config.get(i[0], 'type').strip() == 'mysql':
                                            db = pymysql.connect(host=self.config.get(i[0], 'host'), port=int(self.config.get(i[0], 'port')), user=self.config.get(i[0], 'user'), password=self.config.get(i[0], 'password'), db=self.config.get(i[0], 'db'))
                                    cursor = db.cursor()
                                    if i[2] != 'none' and cursor.execute(self.config.get('sql', i[1])) > 0:
                                        data = cursor.fetchone()
                                        if data == None:
                                            raise Exception('该sql没有返回值：' + self.config.get('sql', i[1]))
                                        else:
                                            data = data[0]
                                        if 'json' in i[1]:
                                            can_shu = i[1].split('_')[(-1)]
                                            try:
                                                data = json.loads(data)
                                            except:
                                                data = 'sql返回的参数不是json格式'
                                            else:
                                                data = sql_json(data, can_shu)

                                        try:
                                            change_data = str(data).decode('gb2312')
                                        except:
                                            change_data = str(data)
                                        else:
                                            try:
                                                self.simple_data = self.simple_data.replace(guid[k], change_data)
                                            except:
                                                pass

                                    elif i[2] == 'none':
                                        cursor.execute(self.config.get('sql', i[1]))
                                        db.commit()
                                    else:
                                        error_data = '获取数据库数据失败:' + self.config.get('sql', i[1])
                            elif 'data' in i[0]:
                                try:
                                    data = self.config.get(i[0], i[1])
                                    self.simple_data = self.simple_data.replace(guid[k], str(data))
                                except:
                                    error_data = '获取常量数据失败:' + self.config.get('sql', i[1])

                            elif 'request' in i[0] and self.take_data != ():
                                try:
                                    data = self.take_data[0][i[1]]
                                    self.simple_data = self.simple_data.replace(guid[k], str(data))
                                except:
                                    error_data = '获取请求数据失败:' + self.config.get('sql', i[1])

                    if type_guid_simple != 0:
                        if type_guid_simple in ('str', 'int', 'float', 'long'):
                            if error_data != '':
                                self.simple_data = error_data
                            elif type_guid_simple.strip() == 'str' and error_data == '':
                                self.simple_data = str(self.simple_data)
                            elif type_guid_simple.strip() == 'int' and error_data == '':
                                try:
                                    self.simple_data = int(float(self.simple_data))
                                except:
                                    pass

                            elif type_guid_simple.strip() == 'float' and error_data == '':
                                try:
                                    self.simple_data = float(self.simple_data)
                                except:
                                    pass

                            elif type_guid_simple.strip() == 'long' and error_data == '':
                                try:
                                    self.simple_data = long(float(self.simple_data))
                                except:
                                    pass

                            elif type_guid_simple.strip() == 'none' and error_data == '':
                                self.simple_data = 'sql_run_success'
                elif '##' not in self.simple_data:
                    pattern = '(\\[.*?\\]\\[.*?\\]\\[.*?\\])'
                    guid = re.findall(pattern, self.simple_data, re.M)
                    type_re = '(\\[.*?\\])'
                    try:
                        type_guid_simple = re.findall(type_re, self.simple_data, re.M)[(-1)][1:-1]
                    except:
                        pass
                    else:
                        error_data = ''
                        if len(guid) > 0:
                            guit = [ i[1:-1].split('][') for i in guid ]
                            for k, i in enumerate(guit):
                                if 'db' in i[0]:
                                    db = pymysql.connect(self.config.get(i[0], 'ip'), self.config.get(i[0], 'name'), self.config.get(i[0], 'password'))
                                    cursor = db.cursor()
                                    if cursor.execute(self.config.get('sql', i[1])) > 0:
                                        data = cursor.fetchone()[0]
                                        if 'json' in i[1]:
                                            can_shu = i[1].split('_')[(-1)]
                                            try:
                                                data = json.loads(data)
                                            except:
                                                data = 'sql返回的参数不是json格式'
                                            else:
                                                data = sql_json(data, can_shu)

                                    else:
                                        error_data = '获取数据库数据失败:' + self.config.get('sql', i[1])
                                else:
                                    if 'data' in i[0]:
                                        try:
                                            data = self.config.get(i[0], i[1])
                                        except:
                                            error_data = '获取常量数据失败'

                                    else:
                                        if 'request' in i[0] and self.take_data != ():
                                            try:
                                                data = self.take_data[0][i[1]]
                                            except:
                                                error_data = '获取请求数据失败:' + self.config.get('sql', i[1])

                                if i[(-1)] in ('str', 'int', 'float', 'long'):
                                    if error_data != '':
                                        pass
                                    elif i[(-1)] == 'str' and error_data == '':
                                        self.simple_data = self.simple_data.replace(guid[k], "'" + str(data) + "'")
                                    elif type_guid_simple.strip() == 'int' and error_data == '':
                                        try:
                                            self.simple_data = self.simple_data.replace(guid[k], str(int(data)))
                                        except:
                                            pass

                                    elif type_guid_simple.strip() == 'float' and error_data == '':
                                        try:
                                            self.simple_data = self.simple_data.replace(guid[k], str(float(data)))
                                        except:
                                            pass

                                    elif type_guid_simple.strip() == 'long' and error_data == '':
                                        try:
                                            self.simple_data = self.simple_data.replace(guid[k], str(float(data)))
                                        except:
                                            pass

                                    elif type_guid_simple.strip() == 'none' and error_data == '':
                                        self.simple_data = 'sql_run_success'

                        try:
                            self.simple_data = eval(re.findall('(\\(.*?\\))', self.simple_data, re.M)[0][1:-1])
                            print type_guid_simple
                        except:
                            pass

                        if type_guid_simple == 'str':
                            self.simple_data = str(self.simple_data)
                        elif type_guid_simple == 'int':
                            self.simple_data = int(float(self.simple_data))
                        elif type_guid_simple == 'float':
                            self.simple_data = float(self.simple_data)
                        elif type_guid_simple == 'long':
                            self.simple_data = long(float(self.simple_data))
                        elif type_guid_simple == 'none':
                            self.simple_data = 'sql_run_success'
            try:
                self.simple_data = json.dumpas(self.simple_data)
            except:
                pass

        return self.simple_data


def sql_json(a, b):
    for i in a:
        if type(i) not in [list, dict, bool]:
            if i.strip() == b.strip():
                return a[i]
        else:
            if type(i) == dict:
                sql_json(a[i], b)
            if type(i) == list:
                for z in b[i]:
                    if type(z) == dict:
                        sql_json(z, b)


def cuowu_reson(data):
    if os.path.isfile(data[0]):
        if os.path.basename(data[0]).strip() == 'excel_data.py' and data[(-1)].strip() == 'han_shu':
            return 'excel中该case的python代码运行错误'
        if os.path.basename(data[0]).strip() == 'change_request_before.py':
            if str(data[3]).strip() == "AttributeError: 'read_data' object has no attribute 'config_path'":
                return 'excel中该case的前置接口目录找不到'
            return 'excel中该case的前置接口运行错误'
        else:
            if os.path.basename(data[0]).strip() == 'assert_run.py':
                return 'excel中该case的断言与返回数据匹配时发生错误'
            if os.path.basename(data[0]).strip() == 'assert_run.py':
                return 'excel中该case的断言与返回数据匹配时发生错误'
            if os.path.basename(data[0]).strip() == 'request_run.py':
                return 'excel中该case的发送请求时发生错误'
            if os.path.basename(data[0]).strip() == 'excel_data.py' and data[3].strip() == 'IndexError: list index out of range':
                return 'excel中该case的存储常量save_data发生错误，预估错误原因：该关键字错误'
            if os.path.basename(data[0]).strip() == 'excel_data.py' and data[2].strip() == 'han_shu':
                return 'excel中该case的自动生成数据关键字编写错误'
            if os.path.basename(data[0]).strip() == 'excel_data.py' and data[2].strip() == 'change_data' and 'local variable' in data[3] and 'db' in data[3] and 'referenced before assignment' in data[3]:
                return '确认数据库连接字符是否正确'
            if os.path.basename(data[0]).strip() == 'excel_data.py' and data[2].strip() == 'change_data' and '该sql没有返回值' in data[3]:
                return '执行sql未获取返回值'
            if 'sql断言失败' in data[3]:
                return 'before_sql 或after_sql 中执行sql失败'
            if 'ValueError: No JSON object could be decoded' in data[3]:
                return '接口请求返回的不是json字符串'
            if "UnboundLocalError: local variable 'data_value' referenced before assignment" in data[3] and os.path.basename(data[0]).strip() == 'excel_data.py':
                return 'save_data找不到要保存的数据'
            if '找不到需要保存的参数' in data[3]:
                return 'save_data找不到要保存的数据'
            return '未知错误'
    else:
        return '未知错误'