import socketio
from edit import Edit  # type: ignore
sio = socketio.Client()


def logger(value: str, args: list[str]):
    _ = ''.join(['[%s]' % s for s in args])
    sio.emit('python_logger', value)
    print(_)
    return _


@sio.event
def connect():
    sio.emit('define_client', 'python')


@sio.event
def edit(clip: int) -> None:
    pass


@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('ws://localhost:8080')
sio.wait()
