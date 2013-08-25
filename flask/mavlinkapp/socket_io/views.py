from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
from gevent import monkey

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
        super(MAVLinkNamespace, self).__init__(environ, ns_name)

    def initialize(self):
        self.log("Socketio session started")

    def log(self, message):
        self.context.app.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def recv_disconnect(self):
        # Remove nickname from the list.
        self.log('Disconnected')
        self.broadcast_event('announcement', '%s has disconnected' % self.session)
        self.disconnect(silent=True)
        return True

    def on_user_message(self, msg):
        self.log('User message: {0}'.format(msg))
        self.broadcast_event('normal_msg', '%s' % msg)
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
