from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
import gevent
from gevent import monkey
import zmq
import json

from flask import Flask, Blueprint, Response, request, render_template, url_for, redirect
from flask import current_app

mod = Blueprint('socket_io', __name__, template_folder='templates', url_prefix='/socket.io')

monkey.patch_all()

class MAVLinkNamespace(BaseNamespace, BroadcastMixin):
    def __init__(self, environ, ns_name, request=None):
        #we need access to the application context so the app is passed in
        #as the request, bit of a hack

        app = request
        self.context = None
        if app:
            self.context = app.request_context(environ)
            self.context.push()
            app.preprocess_request()
        self.zmq_stream_task = None
        super(MAVLinkNamespace, self).__init__(environ, ns_name)

    def initialize(self):
        self.log("Socketio session started")
        context = zmq.Context()
        self.sock = context.socket(zmq.SUB)
        #self.sock.setsockopt(zmq.SUBSCRIBE, "")
        self.sock.connect("tcp://127.0.0.1:5560")

    def log(self, message):
        self.context.app.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def recv_disconnect(self):
        self.log('Disconnected')
        self.g_zmq_stream.kill()
        self.sock.close()
        self.disconnect(silent=True)
        return True

    def on_user_message(self, msg):
        self.log('User message: {0}'.format(msg))
        self.broadcast_event('normal_msg', '%s' % msg)
        return True

    def zmq_stream(self):
        self.log('zmq stream started')
        while True:
            try:
                gevent.sleep(0.01)
                topic = self.sock.recv(zmq.DONTWAIT)
                messagedata = self.sock.recv_pyobj()
                #self.log('MAVLink msg: %s' % messagedata)
                self.emit('announcement', json.dumps(messagedata.to_dict()))
            except Exception, e:
                if e.errno == zmq.EAGAIN:
                    #this error number is caught if a msg is not recv
                    #this is expected
                    pass
                else:
                    self.log(e)
                    return
                
    def on_zmq_sub(self,msg):
        try:
            self.sock.setsockopt_string(zmq.SUBSCRIBE,msg)
            self.log('Subscribed to: %s' % msg)
        except Exception,e:
            print e
            self.log('Could not subscribe to: %s' % msg)
        return True

    def on_zmq_unsub(self, msg):
        try:
            self.sock.setsockopt_string(zmq.UNSUBSCRIBE,msg)
            self.log('Unsubscribed from: %s' % msg)
        except Exception, e:
            self.log('Could not unsubscribe from: %s' % msg)
        return True

    def on_stream_zmq(self, msg):
        self.g_zmq_stream = gevent.spawn(self.zmq_stream)
        return True

@mod.route('/<path:remaining>')
def socketio(remaining):
    #we need access to the app for logging
    app = current_app._get_current_object()
    try:
        socketio_manage(request.environ, {'/mavlink': MAVLinkNamespace}, app)
    except:
        app.logger.error("Exception while handling socketio connection",
                         exc_info=True)
    return Response()
