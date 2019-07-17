# -*- coding: utf-8 -*-

from flask import Flask # 引入 flask
from flask import Flask, request, redirect, url_for
from werkzeug import *
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
app = Flask(__name__)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
app.config.from_object('fileconfig')
db = SQLAlchemy(app)# 实例化一个flask 对象
app.config.from_object('fileconfig')
UPLOAD_FOLDER = r'D:\untitled6\app\Uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
from app import view
