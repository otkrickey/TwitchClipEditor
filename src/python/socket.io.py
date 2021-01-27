import eventlet
import socketio
import json

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/socket.io.js': 'C:/Users/rtkfi/OneDrive/デスクトップ/TwitchClipEditor/src/javascript/socket.io.js',
})

client_sid: dict[str] = {'node': None, 'web': None, }


def log(sid: str, value: str, *args: str, ):
    _ = ''.join(['[%s]' % s for s in args])
    sio.emit('python_logger', value, room=sid)
    print(_)
    return _


def exe_edit(value: int) -> None:
    log(client_sid['node'], 'Server Opened', 'python', 'logger')
    for i in range(value):
        sio.emit('python_executing', i, room=client_sid['web'])
    log(client_sid['node'], 'Server Opened', 'python', 'logger')


@sio.event
def connect(sid: str, environ):
    sio.emit('python_logger', 'connected to %s' % sid, room=sid)
    print('connect ', sid)


@sio.event
def define_client(sid: str, value):
    client_sid[value] = sid
    print('[python][sid] => ' + json.dumps(client_sid))


@sio.event
def python_start_request(sid: str, value):
    print('[python][ctrl] => `Request accepted.`')
    sio.emit('python_start_request', '[python][ctrl] => `Request accepted.`', room=client_sid['nodejs'])
    exe_edit(value)


@sio.event
def disconnect(sid):
    client_sid.pop([k for k, v in client_sid.items() if v == sid][0])
    print("[python][sid] => " + json.dumps(client_sid))
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 8256)), app)
