import socketio

sio = socketio.Client()


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
