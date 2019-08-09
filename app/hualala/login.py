# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: E:\HGTP_server\app\hualala\login.py
# Compiled at: 2017-08-21 17:33:59
__author__ = 'SUNZHEN519'
from tempfile import mktemp
from app import app
from flask import send_from_directory, send_file, Response
import socket, paramiko, os, json, urllib.request, urllib.error, urllib.parse, re, chardet, time, sqlite3
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
import datetime

def login_exe(func):

    def login_do():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        if request.method == 'GET':
            db.close()
            return render_template('/hualala/login.html')
        ip = request.remote_addr
        name = request.form['name']
        passs = request.form['password']
        print(1111111111111111)
        print(name)
        print(passs)
        user_check = cu.execute('select * from user where name="%s" and pass="%s" ' % (name, passs)).fetchall()
        if len(user_check) != 0:
            db.commit()
            cu.executemany('update  user  set time=? ,ip=? where name=?', [(time.time(), ip, name)])
            db.commit()
            db.close()
            return redirect(url_for('first_page_exe'))
        db.close()
        return render_template('/hualala/login.html')

    return login_do