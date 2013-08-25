$(function() {

    var WEB_SOCKET_SWF_LOCATION = '/static/js/socketio/WebSocketMain.swf',
        socket = io.connect('/mavlink');

    socket.on('connect', function () {
//        $('#rawlog').addClass('connected');
        socket.emit('stream zmq', '');
    });

    socket.on('announcement', function (msg) {
        $('#lines').prepend($('<p>').append($('<em>').text(msg)));
    });
    socket.on('normal_msg', function (msg) {
        $('#lines').append($('<p>').text(msg));
    });
    socket.on('reconnect', function () {
        $('#lines').remove();
        message('System', 'Reconnected to the server');
    });
    socket.on('reconnecting', function () {
        message('System', 'Attempting to re-connect to the server');
    });
    socket.on('error', function (e) {
        message('System', e ? e : 'A unknown error occurred');
    });

    // DOM manipulation
    $(function () {
        $('#subscribe').submit(function () {
            socket.emit('zmq sub', $('#sub_topic').val());
            return false;
        });
        $('#unsubscribe').submit(function () {
            socket.emit('zmq unsub', $('#unsub_topic').val());
            return false;
        });
    });
});
