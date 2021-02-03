import socketio
import subprocess

# Fix Path Bugs
Path = True
if Path: from tools import *
else: from src.python.tools import *


sio = socketio.Client()


def Edit(PATH: str, clip: int, textContent: str) -> None:
    """
    Edit Video
    --------------------------------

    Parameters:

               clip: int       - Twitch Clip ID
        textContent: str       - Text to display
           callback: callable  - Callable for LoggerFunction

    Returns:

        None

    Attribute:

           filename: str         - Video File Name
        INPUT VIDEO: Video       - Input Video (Downloaded Video)
        INPUT VIDEO: Video       - Input Video (Export Video)
         FrameCount: int         - Input Video Frame Count
         RectImage1: np.ndarray  - BackGroundImage
         RectImage2: np.ndarray  - UnderLineImage
         TextImage3: np.ndarray  - FrontText
        FrontImage1: tuple(np.ndarray, tuple(int, int))  - Position of RectImage1
        FrontImage2: tuple(np.ndarray, tuple(int, int))  - Position of RectImage2
        FrontImage3: tuple(np.ndarray, tuple(int, int))  - Position of TextImage3
    """
    filename = f'clip-{clip}.mp4'
    INPUT_VIDEO = cv2.VideoCapture(f'{PATH}download/{filename}')
    OUTPUT_VIDEO = cv2.VideoWriter(f'{PATH}export/{filename}', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 60, (1920, 1080))
    FrameCount = int(INPUT_VIDEO.get(cv2.CAP_PROP_FRAME_COUNT))
    RectImage1 = Rect((360, 120), (197, 22, 92), radius=8).image
    RectImage2 = Rect((360, 10), (255, 255, 255), radius=5).image
    TextImage3 = Text((360, 120), (255, 255, 255), textContent).image
    FrontImage1 = Position(RectImage1, (0, 60), (-340, 60), (20, 60))
    FrontImage2 = Position(RectImage2, (15, 75), (-340, 170), (20, 170))
    FrontImage3 = Position(TextImage3, (30, 90), (-340, 60), (20, 60))
    for i in range(FrameCount):
        flag, frame = INPUT_VIDEO.read()
        if not flag: break
        frame = mask(frame, *FrontImage1.t(i))
        frame = mask(frame, *FrontImage2.t(i))
        frame = mask(frame, *FrontImage3.t(i))
        OUTPUT_VIDEO.write(frame)
        sio.emit('editor', i)
    INPUT_VIDEO.release()
    OUTPUT_VIDEO.release()
    subprocess.call(f'ffmpeg -i {PATH}export/{filename} -i {PATH}download/{filename} -c:v copy {PATH}{filename} -loglevel quiet -y')


def logger(value: str, args: list[str]):
    _ = ''.join(['[%s]' % s for s in args])
    sio.emit('python_logger', value)
    print(_ + value)
    return _


@sio.event
def connect():
    sio.emit('define_client', 'python')


@sio.event
def edit(clip) -> None:
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
