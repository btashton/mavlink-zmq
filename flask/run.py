from mavlinkapp import app
from gevent import monkey
from socketio.server import SocketIOServer


monkey.patch_all()

PORT = 5000

if __name__ == '__main__':
    SocketIOServer(('', PORT), app, resource="socket.io").serve_forever()

