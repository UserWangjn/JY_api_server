# -*- coding: utf-8 -*-

from flask import Flask # 引入 flask
from flask import Flask, request, redirect, url_for
from werkzeug import *
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('fileconfig')
db = SQLAlchemy(app)# 实例化一个flask 对象
app.config.from_object('fileconfig')
UPLOAD_FOLDER = r'D:\untitled6\app\Uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from app import view
