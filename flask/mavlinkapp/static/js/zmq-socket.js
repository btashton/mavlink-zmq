$(function() {

    var WEB_SOCKET_SWF_LOCATION = '/static/js/socketio/WebSocketMain.swf',
        socket = io.connect('/mavlink');

    socket.on('connect', function () {
        $('#rawlog').addClass('connected');
    });

    socket.on('announcement', function (msg) {
        $('#lines').append($('<p>').append($('<em>').text(msg)));
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
    function message (from, msg) {
        $('#lines').append($('<p>').append($('<b>').text(from), msg));
    }

    // DOM manipulation
    $(function () {
        $('#send-message').submit(function () {
            socket.emit('user message', $('#message').val());
            return false;
        });
    });
});
