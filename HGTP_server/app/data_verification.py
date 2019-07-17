# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\jieyuelianhe\old_all_server\HGTP_server\app\data_verification.py
# Compiled at: 2018-08-23 09:48:54
__author__ = 'SUNZHEN519'
from selenium import webdriver
import time, chardet, unittest, demjson, urllib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import unittest, xlrd, json, urllib2, os

class read_excel(object):

    def __init__(self, file):
        self.data = xlrd.open_workbook(file)
        self.table0 = self.data.sheets()[0]
        self.key0 = self.table0.row_values(0)
        self.data0 = [ self.table0.row_values(i) for i in range(1, self.table0.nrows) ]
        self.table0 = self.table0.row_values(0)
        self.table1 = self.data.sheets()[1]
        self.key1 = self.table1.row_values(0)
        self.data1 = [ self.table1.row_values(i) for i in range(1, self.table1.nrows) ]
        self.table1 = self.table1.row_values(0)
        self.table2 = self.data.sheets()[2]
        self.key2 = self.table2.row_values(0)
        self.data2 = [ self.table2.row_values(i) for i in range(1, self.table2.nrows) ]
        self.table2 = self.table2.row_values(0)


class read_mysql(object):

    def __init__(self, sql):
        self.conn = MySQLdb.connect(host='10.199.129.247', port=3309, user='vis', passwd='vispvip', db='visAdmin', cursorclass=MySQLdb.cursors.DictCursor)
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.data = self.cur.fetchone()
        self.conn.close()


class pipei(object):

    def __init__(self, a, b):
        self.error = {}
        for i in a.keys():
            if a[i].strip() == b[i].strip():
                pass
            else:
                self.error[i] = a.keys