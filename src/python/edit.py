import subprocess
from typing import Tuple, Union

import cv2
import numpy as np
from matplotlib import pyplot as plt
from src.python.createImage import Rect, Text
from src.python.easing import Easing


class Image:
    def __init__(self, image: np.ndarray, timing: tuple[int, int], start_position: tuple, end_position: tuple) -> None:
        self.image = image
        self.st = timing[0]
        self.et = timing[1]
        self.spx = start_position[0]
        self.spy = start_position[1]
        self.epx = end_position[0]
        self.epy = end_position[1]

    def position(self, t) -> tuple[np.ndarray, tuple]:
        if t < self.st:
            return (self.image, (self.spx, self.spy))
        elif self.st <= t < self.et:
            return (self.image, (int(self.spx if self.spx == self.epx else Easing((t - self.st) / (self.et - self.st)).easeInOutBack * (self.epx - self.spx) + self.spx),
                                 int(self.spy if self.spy == self.epy else Easing((t - self.st) / (self.et - self.st)).easeInOutBack * (self.epy - self.spy) + self.spy)))
        else:
            return (self.image, (self.epx, self.epy))


def mask(back: np.ndarray, front: np.ndarray, position: tuple) -> np.ndarray:
    '''
    `back`に指定された画像に`front`に指定した画像を`position`で指定した位置に合成する。

    Parameters
    ----------
    back : np.ndarray
        背景画像。後ろ側の画像。
    front : np.ndarray
        合成画像。手間側の画像。
    position : tuple
        合成する位置。`back`に指定した画像の左上を基準に横軸x、縦軸yで指定する。
        `front`に指定した画像の左上の場所を指す。

    Returns
    -------
    back : np.ndarray
        合成後の背景画像。
    '''
    px, py = position
    fh: int = front.shape[0]
    fw: int = front.shape[1]
    bh: int = back.shape[0]
    bw: int = back.shape[1]
    px1: int = max(px, 0)
    py1: int = max(py, 0)
    px2: int = min(px + fw, bw)
    py2: int = min(py + fh, bh)
    # 合成画像が範囲外の場合
    if not ((-fw < px < bw) and (-fh < py < bh)):
        return back
    front3: np.ndarray = front[..., : 3]
    mask1: np.ndarray = front[..., 3]
    mask3: np.ndarray = cv2.merge((mask1, mask1, mask1))
    mask_roi: np.ndarray = mask3[py1 - py: py2 - py, px1 - px: px2 - px]
    front_roi: np.ndarray = front3[py1 - py: py2 - py, px1 - px: px2 - px]
    roi: np.ndarray = back[py1:py2, px1:px2]
    tmp1: np.ndarray = cv2.bitwise_and(roi, mask_roi)
    tmp2: np.ndarray = cv2.bitwise_or(tmp1, front_roi)
    back[py1:py2, px1:px2] = tmp2
    return back


class Edit:
    def __init__(self, clip_id: int, textContent: str, FILE_PATH: str) -> None:
        filename = f'clip-{clip_id}.mp4'
        self.filename = filename
        self.FILE_PATH = FILE_PATH
        self.InputVideo = cv2.VideoCapture(f'{FILE_PATH}download/{self.filename}')
        self.OutPutVIdeo = cv2.VideoWriter(f'{FILE_PATH}export/{self.filename}', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 60, (1920, 1080))
        self.FrameCount = int(self.InputVideo.get(cv2.CAP_PROP_FRAME_COUNT))
        # call 3 images here
        self.Rect1 = Rect((360, 120), (197, 22, 92), radius=8).image
        self.Rect2 = Rect((360, 10), (255, 255, 255), radius=5).image
        self.Text3 = Text((360, 120), (255, 255, 255), textContent).image
        self.FrontImage1 = Image(self.Rect1, (0, 60), (-340, 60), (20, 60))
        self.FrontImage2 = Image(self.Rect2, (15, 75), (-340, 170), (20, 170))
        self.FrontImage3 = Image(self.Text3, (30, 90), (-340, 60), (20, 60))

    def edit(self):
        for i in range(self.FrameCount):
            flag, frame = self.InputVideo.read()
            if not flag: break
            frame = mask(frame, *self.FrontImage1.position(i))
            frame = mask(frame, *self.FrontImage2.position(i))
            frame = mask(frame, *self.FrontImage3.position(i))
            self.OutPutVIdeo.write(frame)
            if i % 100 == 0: print(i)
        self.InputVideo.release()
        self.OutPutVIdeo.release()
        subprocess.call(
            f'ffmpeg -i {self.FILE_PATH}export/{self.filename} -i {self.FILE_PATH}download/{self.filename} -c:v copy {self.FILE_PATH}{self.filename} -loglevel quiet -y'
        )


FILE_PATH = 'src/video/'


def edit(self, clip_id: int, textContent: str) -> None:
    filename = f'clip-{clip_id}.mp4'
    INPUT_VIDEO = cv2.VideoCapture(f'{FILE_PATH}download/{filename}')
    OUTPUT_VIDEO = cv2.VideoCapture(f'{FILE_PATH}export/{filename}', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 60, (1920, 1080))
    FrameCount = int(INPUT_VIDEO.get(cv2.CAP_PROP_FRAME_COUNT))
    RectImage1 = Rect((360, 120), (197, 22, 92), radius=8).image
    RectImage2 = Rect((360, 10), (255, 255, 255), radius=5).image
    TextImage3 = Text((360, 120), (255, 255, 255), textContent).image
    FrontImage1 = Image(self.Rect1, (0, 60), (-340, 60), (20, 60))
    FrontImage2 = Image(self.Rect2, (15, 75), (-340, 170), (20, 170))
    FrontImage3 = Image(self.Text3, (30, 90), (-340, 60), (20, 60))
    for i in range(FrameCount):
        flag, frame = INPUT_VIDEO.read()
        if not flag: break
        frame = mask(frame, *FrontImage1.position(i))
        frame = mask(frame, *FrontImage2.position(i))
        frame = mask(frame, *FrontImage3.position(i))
        OUTPUT_VIDEO.write(frame)
    INPUT_VIDEO.release()
    OUTPUT_VIDEO.release()
    subprocess.call(f'ffmpeg -i {FILE_PATH}export/{filename} -i {FILE_PATH}download/{filename} -c:v copy {FILE_PATH}{filename} -loglevel quiet -y')


def main():
    Edit(991466429, 'Streamer Name', 'src/video/').edit()
    pass


if __name__ == '__main__': main()
