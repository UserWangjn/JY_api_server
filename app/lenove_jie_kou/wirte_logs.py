# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
# [GCC 8.2.1 20181127]
# Embedded file name: C:\jieyuelianhe\old_all_server\HGTP_server\app\lenove_jie_kou\wirte_logs.py
# Compiled at: 2019-02-21 11:38:53
__author__ = 'SUNZHEN519'
from tempfile import mktemp
from assert_run import *
from app import app
from flask import send_from_directory, send_file, Response
import socket, os, time, sqlite3
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from flask import current_app
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
import json, demjson
from functools import wraps

def dwirte_logs(func):

    def ceshi():
        linux = g.cu.execute('select linux from jie_kou_test where name="%s" and ip="%s"' % (request.form['name'], ip)).fetchall()[0][0]
        linux = eval(linux)
        hostname = linux['ip']
        username = linux['username']
        password = linux['password']
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname, 22, username, password, timeout=5)
        s.close()

    return ceshi