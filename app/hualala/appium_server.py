# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\jieyuelianhe\old_all_server\HGTP_server\app\hualala\appium_server.py
# Compiled at: 2018-12-18 10:42:36
__author__ = 'SUNZHEN519'
from tempfile import mktemp
from app import app
from flask import send_from_directory, send_file, Response
import socket, os, json, urllib.request, urllib.error, urllib.parse, re, chardet, time, sqlite3
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
import datetime, requests

def appium_server(fun):

    def appium_server():
        fun()
        case_url = 'http://' + current_app.config.get('APPIUM_IP') + '/cases'
        response = requests.get(case_url)
        case_json = json.loads(response.text)['cases']
        print(9999999999999999999999999999999)
        print(case_json)
        return render_template('/hualala/jiekou_test/appium_url.html', case_json=case_json)

    return appium_server