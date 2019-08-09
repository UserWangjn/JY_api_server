# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\Users\sunzhen\Desktop\web flask\HGTP_socket3\app\jie_kou_test\json_pi_pei\before_after_sql.py
# Compiled at: 2019-04-09 19:19:24
__author__ = 'SUNZHEN519'
import sys, re, requests, json, datetime
from selenium import webdriver
import time, chardet, unittest, demjson, pymysql, urllib.request, urllib.parse, urllib.error
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import unittest, xlrd, json, urllib.request, urllib.error, urllib.parse, os, logging, random, pymysql
from .excel_data import *

def before_after_sql(sql_detail, config):
    type_re = '(\\[.*?\\]\\[.*?\\]\\[.*?\\])'
    for i in sql_detail.split(','):
        if len(re.findall(type_re, i, re.M)) == 0:
            i = i + '[none]'
            s = change_data_db(config, i)
        else:
            if len(re.findall(type_re, i, re.M)) > 0:
                s = change_data_db(config, i)
        assert_str = s.simple_data.replace('[none]', '')
        statu = 0
        for i in ['==', '<', '>', '>=', '<=', '!=']:
            if i in assert_str:
                assert_str = i.join([ "'" + str(i).strip() + "'" for i in assert_str.split(i) ])
                statu = 1
                break

        print(9999999999999999999999999999999999999999999999999999999)
        print(assert_str)
        if statu == 1:
            if not eval(assert_str):
                ex = Exception('sql断言失败%s' % s.simple_data.replace('[none]', ''))
                raise ex

    return {'statu': 'success'}