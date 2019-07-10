# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\jieyuelianhe\old_all_server\HGTP_server\app\hualala\check_login.py
# Compiled at: 2018-11-08 11:24:40
__author__ = 'SUNZHEN519'
from tempfile import mktemp
from app import app
from flask import send_from_directory, send_file, Response
import socket, os, json, urllib2, re, chardet, time, sqlite3
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
import datetime

def check_login():
    ip = request.headers.get('X-Real-IP')
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    login_check = cu.execute('select time from user where  ip="%s" ' % ip).fetchall()
    db.close()
    if len(login_check) == 0:
        return render_template('/hualala/login.html')