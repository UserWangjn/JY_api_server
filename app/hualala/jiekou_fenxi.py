# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\jieyuelianhe\old_all_server\HGTP_server\app\hualala\jiekou_fenxi.py
# Compiled at: 2019-02-26 13:31:48

from tempfile import mktemp
from app import app
from flask import send_from_directory, send_file, Response
import socket, os, json, urllib.request, urllib.error, urllib.parse, re, chardet, time, sqlite3
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
import datetime, xlrd, xlwt

def jiekou_fenxi_shouye(func):

    def jiekou_fenxi_shouye():
        func()
        return render_template('/hualala/jiekou_test/jiekou_fenxi.html')

    return jiekou_fenxi_shouye