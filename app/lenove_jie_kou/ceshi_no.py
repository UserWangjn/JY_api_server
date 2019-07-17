# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
# [GCC 8.2.1 20181127]
# Embedded file name: C:\jieyuelianhe\old_all_server\HGTP_server\app\lenove_jie_kou\ceshi_no.py
# Compiled at: 2018-08-23 09:49:41
__author__ = 'SUNZHEN519'
com = 'python D:\\efq_ben\\mulu.py'
from tempfile import mktemp
from app import app
from flask import send_from_directory, send_file, Response
import socket, os, time, sqlite3
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from flask import current_app
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
import json, demjson
from functools import wraps

def ceshi_no(func):

    def aa():
        func()
        ip = '127.0.0.1'
        if len(g.cu.execute('select * from jie_kou_test where  ip="%s" and num="run"' % ip).fetchall()) == 0:
            bug = [
             'no data', 'no data']
        else:
            data = g.cu.execute('select * from jie_kou_test where  ip="%s" and num="run"' % ip).fetchall()[0]
            bug = [ json.dumps(json.loads(json.dumps(demjson.decode(i)), parse_int=int), indent=4, sort_keys=False, ensure_ascii=False) for i in data[3].split('##')
                  ]
            bug.append(data[1])
        if len(g.cu.execute('select * from jie_kou_test where  ip="%s" and num="bug"' % ip).fetchall()) == 0:
            debug = [
             'no data', 'no data']
        else:
            data = g.cu.execute('select * from jie_kou_test where  ip="%s" and num="bug"' % ip).fetchall()[0]
            debug = [ json.dumps(json.loads(json.dumps(demjson.decode(i)), parse_int=int), indent=4, sort_keys=False, ensure_ascii=False) for i in data[3].split('##')
                    ]
            debug.append(data[1])
        if request.method == 'GET':
            return render_template('/simple_page/ceshi_p.html', a=bug[:2], b=debug[:2], c=bug[(-1)], d=debug[(-1)])
        if request.method == 'POST':
            return jsonify(a=bug[0], b=bug[1], c=debug[0], d=debug[1], bugname=data[1])
        return [bug, debug]

    return aa