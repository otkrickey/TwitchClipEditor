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


def logger(value: str, args: list[str]):
    _ = ''.join(['[%s]' % s for s in args])
    sio.emit('python_logger', value, room=client_sid['nodejs'])
    print(_)
    return _


def exe_edit(value: int) -> None:
    for i in range(value):
        sio.emit('python_Editing', i, room=client_sid['chrome'])


@sio.event
def connect(sid: str, environ):
    logger('Connected: %s' % sid, ['python'])


@sio.event
def define_client(sid: str, value):
    client_sid[value] = sid
    logger('%s: %s' % (value, sid), ['python', 'define_client'])


@sio.event
def StartEdit(sid: str, value):
    logger('Editor Started', ['python', 'logger'])
    exe_edit(value)
    logger('Editor Finished', ['python', 'logger'])


@sio.event
def disconnect(sid):
    client_sid.pop([k for k, v in client_sid.items() if v == sid][0])
    print("[python][sid] => " + json.dumps(client_sid))
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', int(args.port))), app)
