# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\jieyuelianhe\old_all_server\THREAD_BEIFEN\THREAD_fuben\jie_kou_test\pi_run\all_run.py
# Compiled at: 2019-05-05 11:50:08
__author__ = 'SUNZHEN519'
import sys, os
sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))
from selenium import webdriver
import time, chardet, unittest, demjson, urllib.request, urllib.parse, urllib.error
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import unittest, xlrd, json, urllib.request, urllib.error, urllib.parse, os, logging, random
from json_pi_pei.json_pi_pei import *
from json_pi_pei.request_run import *
from assert_run.assert_run import *
from .pi_run import *
from json_pi_pei.begin_excel import reead_excel

class run(object):

    def __init__(self, path, run_time, *ip):
        self.all = {}
        self.suite = []
        for i in path:
            if i[1] not in list(self.all.keys()):
                self.all[i[1]] = [
                 i[0]]
            else:
                self.all[i[1]].append(os.path.normpath(i[0]))

        if len(ip) != 0:
            self.ip = ip[0]
            self.server_ip = ip[1]
            self.run_id = ip[2]
        self.time = run_time
        self.num = 0
        path = [ i[0].decode('utf-8') for i in path ]
        for git, mulu in list(self.all.items()):
            self.all_bianliang = {}
            self.u = reead_excel(mulu)
            self.all_bianliang['before_case_detail'] = self.u.all_case
            for k, i in enumerate(mulu):
                self.num += 1
                pi_run(i, run_time, self.ip, self.server_ip, self.all_bianliang, self.run_id, git)


if __name__ == '__main__':
    z = []
    z.append('C:\\所写系统\\无时间限制正常程序\\lr_test\\第二套环境\\HGTP\\get接口')
    z.append('C:\\所写系统\\无时间限制正常程序\\lr_test\\测试环境\\HGTP\\post接口')
    run(z, 'C:\\work\\lenove_jie_kou')