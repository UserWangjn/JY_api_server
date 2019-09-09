# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: E:\old_all_server\THREAD\THREAD_fuben\jie_kou_test\just_run\save_global_data.py
# Compiled at: 2019-05-06
import sys
import importlib
sys.path.append('../../')
importlib.reload(sys)
from selenium import webdriver
from .change_request_before import read_data
import time as timee, chardet, unittest, demjson, urllib.request, urllib.parse, urllib.error, random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import unittest, xlrd, configparser, json, urllib.request, urllib.error, urllib.parse, os, logging
from .just_run import *
from excel_data import *
import copy
from json_pi_pei.request_result_flask import *
from json_pi_pei.json_pi_pei import *
from json_pi_pei.request_run import *
from assert_run.assert_run import *

class set_global_data(object):

    def set_global_data(self, excel_dict, config_path, path, all_bianliang):
        if 'global_data' in list(excel_dict.keys()) and excel_dict['global_data'].strip() != '':
            for jiekou in [ i for i in excel_dict['global_data'].split(',') if i.strip() not in list(all_bianliang.keys()) ]:
                self.path = os.path.dirname(path)
                self.config_path = config_path
                self.all = []
                self.data = copy.deepcopy(excel_dict)
                self.all.append(jiekou)
                self.s = read_data(jiekou, self.path).data
                while 'before_request' in self.s and self.s['before_request'].strip() != '':
                    self.all.append(self.s['before_request'])
                    self.s = read_data(self.s['before_request'], self.path).data
                    if not('before_request' in self.s and self.s['before_request'].strip() != ''):
                        break

                self.s = read_data(jiekou, self.path).data
                if '/' in self.all[(-1)]:
                    self.s = just_run(os.path.join(os.path.dirname(self.path), self.all[(-1)].split('$')[0]), self.all[(-1)].split('$')[1], data={}, before_req='', config_path=self.config_path)
                    all_bianliang[self.all[(-1)]] = {'request': self.s.req, 'result': self.s.respons}
                else:
                    self.s = just_run(os.path.join(os.path.dirname(self.path), self.all[(-1)].split('$')[0]), self.all[(-1)].split('$')[1], data={}, before_req='', config_path=self.config_path)
                    all_bianliang[self.all[(-1)]] = {'request': self.s.req, 'result': self.s.respons}
                if 'err_detail' in list(self.s.data.keys()):
                    return self.s.data
                for i in list(reversed(self.all[:-1])):
                    self.s = just_run(os.path.join(os.path.dirname(self.path), i.split('$')[0]), i.split('$')[1], json.loads(self.s.respons), self.s.full_data, self.config_path)
                    all_bianliang[i] = {'request': self.s.req, 'result': self.s.respons}
                    if 'err_detail' in list(self.s.data.keys()):
                        return self.s.data