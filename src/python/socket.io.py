import argparse
import json

import eventlet
import socketio

# Check Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', help='Server Port')
args = parser.parse_args()

# Create Server
sio = socketio.Server()
app = socketio.WSGIApp(sio)

# define client-name and client-id
client_sid: dict[str] = {'nodejs': None, 'chrome': None}


def logger(sid: str, value: str, *args: str):
    _ = ''.join(['[%s]' % s for s in args])
    sio.emit('python_logger', value, room=sid)
    print(_)
    return _


def exe_edit(value: int) -> None:
    logger(client_sid['nodejs'], 'Server Opened', 'python', 'logger')
    for i in range(value):
        sio.emit('python_executing', i, room=client_sid['chrome'])
    logger(client_sid['nodejs'], 'Server Opened', 'python', 'logger')


@sio.event
def connect(sid: str, environ):
    logger(sid, 'Connected. sid = %s' % sid, 'python')


@sio.event
def define_client(sid: str, value):
    client_sid[value] = sid
    print('[python][sid] => ' + json.dumps(client_sid))


@sio.event
def StartEdit(sid: str, value):
    print('[python][ctrl] => `Request accepted.`')
    sio.emit('python_start_request', '[python][ctrl] => `Request accepted.`', room=client_sid['nodejs'])
    exe_edit(value)


@sio.event
def disconnect(sid):
    client_sid.pop([k for k, v in client_sid.items() if v == sid][0])
    print("[python][sid] => " + json.dumps(client_sid))
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', int(args.port))), app)
