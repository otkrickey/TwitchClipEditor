import socketio

from tools import Edit  # type: ignore

sio = socketio.Client()


def ic(value) -> None:
    print(f'{locals()}: {value}')


def logger(value: str, args: list[str]):
    _ = ''.join(['[%s]' % s for s in args])
    sio.emit('python_logger', value)
    print(_)
    return _


@sio.event
def connect():
    sio.emit('define_client', 'python')


@sio.event
def edit(clip) -> None:
    ic(clip)
    for i in range(int(clip)):
        sio.emit('editor', i)
        print(i)


@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('ws://localhost:8080')
sio.wait()
