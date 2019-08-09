# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\jieyuelianhe\old_all_server\HGTP_server\app\jie_kou.py
# Compiled at: 2018-10-19 16:28:46
from tempfile import mktemp
from app import app
from flask import send_from_directory, send_file, Response
import socket, os, json, urllib.request, urllib.error, urllib.parse, re, chardet
from functools import wraps
from .zhixing import *
from .yuansudingwei import *
import time, sqlite3
from .shell_name import *
from .form import *
import demjson
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from flask_bootstrap import Bootstrap
import urllib.request, urllib.parse, urllib.error
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify

class kaifa_run(object):

    def __init__(self, data, req):
        print(777777711111)
        print(req[0])
        print(req[1])
        print(req[2])
        request = urllib.request.Request(req[0])
        request.add_header(req[1], req[2])
        if 'createStockItem' in req[0] or 'autoOnlineDataCheck' in req[0]:
            req_data = {'data': data}
        else:
            req_data = eval(data)
        print(req_data)
        print(type(req_data))
        print(request)
        response = urllib.request.urlopen(request, urllib.parse.urlencode(req_data))
        self.x = response.read()
        self.x = json.dumps(json.loads(json.dumps(demjson.decode(self.x)), parse_int=int), indent=4, sort_keys=False, ensure_ascii=False)