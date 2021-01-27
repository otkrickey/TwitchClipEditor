import eventlet
import socketio
import json

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/socket.io.js': 'C:/Users/rtkfi/OneDrive/デスクトップ/TwitchClipEditor/src/javascript/socket.io.js',
})

client_sid: dict = {}


def log(value: str, *args: str):
    _ = ''
    for s in args: _ += '[%s]' % s
    _ += ' %s' % value
    print(_)
    return _


def exe_edit(sid, value):
    log('Server Started', 'python', 'ctrl')
    for i in range(value):
        sio.emit('python_executing', i, room=client_sid['web_client'])
    log('Server Finished', 'python', 'ctrl')


@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.event
def define_client(sid, value):
    client_sid[value] = sid
    print('[python][sid] => ' + json.dumps(client_sid))


@sio.event
def python_start_request(sid, value):
    print('[python][ctrl] => `Request accepted.`')
    sio.emit('python_start_request', '[python][ctrl] => `Request accepted.`', room=client_sid['nodejs_client'])
    exe_edit(sid, value)


@sio.event
def msg(sid, data):
    print('[python][ctrl] => %s' % data)


@sio.event
def disconnect(sid):
    client_sid.pop([k for k, v in client_sid.items() if v == sid][0])
    print("[python][sid] => " + json.dumps(client_sid))
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 8256)), app)
