__author__ = 'SUNZHEN519'
from app import app
__author__ = 'SUNZHEN519'
from app import app
from flask_socketio import SocketIO, emit
socketio = SocketIO()
socketio.init_app(app)
if __name__ == '__main__':
     #socketio.run(app, debug=False, host='0.0.0.0', port=5000, threaded=True)
     app.run(host='0.0.0.0',port=5021,debug='False',threaded=True)


