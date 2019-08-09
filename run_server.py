from flask import Flask,render_template
import os
import sys
from celery import Celery
# from gevent import monkey
# monkey.patch_all()
# from gevent import pywsgi
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app
from gevent import monkey
from gevent.pywsgi import WSGIServer

def run_server():
    app.run(host='0.0.0.0',port=5026,debug=True,threaded=True)

#if __name__ == '__main__':
     #socketio.run(app, debug=False, host='0.0.0.0', port=5000, threaded=True)
#     run_server()
     # server = pywsgi.WSGIServer(('127.0.0.1', 5026), app)
     # server.serve_forever()
     # monkey.patch_all()
     # WSGIServer(('0.0.0.0', 5026), app).serve_forever()

