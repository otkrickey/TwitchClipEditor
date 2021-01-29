import subprocess
from typing import Tuple, Union

import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont

from easing import Easing


class Rect:
    """
    Create Rect Image
    -----------------

    Methods:

        self.image np.ndarray  - Out put image

    Attributes:

        canvas: np.ndarray            - Image Array
          size: tuple(int, int)       - Image Size
         color: tuple(int, int, int)  - Image Color
        radius: float                 - BorderRadius (0 - size / 2)
    """

    def __init__(self, size: tuple[int, int], color: tuple[int, int, int], radius: float) -> None:
        """
        Create Image
        ------------
        Parameters:

              size: tuple(int, int)       - Image Size
             color: tuple(int, int, int)  - Image Color
            radius: tuple(int, float)     - BorderRadius (0 - size / 2)
        """
        self.size = size
        self.color = color
        self.canvas = np.full((size[1], size[0], 4), 0, dtype=np.uint8)
        cv2.rectangle(self.canvas, (radius, radius), (self.size[0] - radius, self.size[1] - radius), self.color, -1, cv2.LINE_AA)
        cv2.rectangle(self.canvas, (radius, radius), (self.size[0] - radius, self.size[1] - radius), self.color, radius * 2, cv2.LINE_AA)
        self.canvas[..., 3] = self.canvas[..., :3].sum(axis=2) / sum(self.color) * 255

    @property
    def image(self) -> np.ndarray:
        """
        Export Image
        ------------

        Returns:

            self.canvas: np.ndarray  - Copy of the Created Image
        """
        return self.canvas.copy()


class Text:
    """
    Create Text Image
    -----------------

    Methods:

        self.image: np.ndarray  - Out put image

    Attributes:

          canvas: np.ndarray            - Image Array
            size: tuple(int, int)       - Image Size
           color: tuple(int, int, int)  - Image Color
         content: str                   - Text to display
        fontsize: float = 36            - FontSize
    """

    def __init__(self, size: tuple[int, int], color: tuple[int, int, int], content: str, fontsize: float = 36) -> None:
        """
        Create Image
        ------------

        Parameters:

                size: tuple(int, int)       - Image Size
               color: tuple(int, int, int)  - Image Color
             content: str                   - Text to display
            fontsize: float = 36            - FontSize
        """
        self.canvas = np.full((size[1], size[0], 4), 0, dtype=np.uint8)
        PIL_Image = Image.fromarray(self.canvas[..., :3])
        draw = ImageDraw.Draw(PIL_Image)
        font = ImageFont.truetype("src/fonts/MPLUSRounded1c-Medium.ttf", fontsize)
        textsize = draw.textsize(content, font=font)
        font_offset = font.getoffset(content)
        px = (size[0] - textsize[0] - font_offset[0]) / 2
        py = (size[1] - textsize[1] - font_offset[1]) / 2
        draw.text((px, py), content, color, font)
        self.canvas[..., :3] = np.array(PIL_Image, dtype=np.uint8)
        self.canvas[..., 3] = self.canvas[..., :3].sum(axis=2) / sum(color) * 255

    @property
    def image(self) -> np.ndarray:
        """
        Export Image
        ------------

        Returns:

            self.canvas: np.ndarray  - Copy of the Created Image
        """
        return self.canvas.copy()


class Position:
    """
    Set Image Position
    ------------------

    Methods:

        self.t(t: int): tuple(np.ndarray, tuple(int, int)) - Position at the time of {t}

    Attributes:

        image: np.ndarray  - Image Array
           st: int         - Start Time
           et: int         -   End Time
           sx: int         - Start Position {x}
           sy: int         -   End Position {y}
           ex: int         - Start Position {x}
           ey: int         -   End Position {y}
    """

    def __init__(self, image: np.ndarray, timing: tuple[int, int], start: tuple[int, int], end: tuple[int, int]) -> None:
        """
        Set Variables
        -------------

        Parameters:

             image: np.ndarray       - Image Array
            timing: tuple(int, int)  - Timing (Start, End)
             start: tuple(int, int)  - Start Position (x, y)
               end: tuple(int, int)  -   End Position (x, y)
        """
        self.image = image
        self.st = timing[0]
        self.et = timing[1]
        self.sx = start[0]
        self.sy = start[1]
        self.ex = end[0]
        self.ey = end[1]

    def t(self, t: int) -> tuple[np.ndarray, tuple[int, int]]:
        """
        Position at the time of {t}
        ---------------------------

        Parameters:

            t: int  - Current Time
        """
        if t < self.st:
            return (self.image, (self.sx, self.sy))
        elif self.st <= t < self.et:
            return (self.image, (int(self.sx if self.sx == self.ex else Easing((t - self.st) / (self.et - self.st)).easeInOutBack * (self.ex - self.sx) + self.sx),
                                 int(self.sy if self.sy == self.ey else Easing((t - self.st) / (self.et - self.st)).easeInOutBack * (self.ey - self.sy) + self.sy)))
        else:
            return (self.image, (self.ex, self.ey))


def mask(back: np.ndarray, front: np.ndarray, position: tuple[int, int]) -> np.ndarray:
    """
    Combine FrontImage and BackImage
    --------------------------------

    Parameters:

            back: np.ndarray       -  Back Image
           front: np.ndarray       - Front Image
        position: tuple(int, int)  - Position of Front Image (x, y)

    Returns:

        back: np.ndarray  - Created Image

    Attribute:

        bh: int  -  BackImage Size {h}
        bw: int  -  BackImage Size {w}
        fh: int  - FrontImage Size {h}
        fw: int  - FrontImage Size {w}
        px: int  -        Position {x}
        py: int  -        Position {y}
        sx: int  -  Start Position {x}
        sy: int  -    End Position {y}
        ex: int  -  Start Position {x}
        ey: int  -    End Position {y}
    """
    bh: int = back.shape[0]
    bw: int = back.shape[1]
    fh: int = front.shape[0]
    fw: int = front.shape[1]
    px: int = position[0]
    py: int = position[1]
    sx: int = max(px, 0)
    sy: int = max(py, 0)
    ex: int = min(px + fw, bw)
    ey: int = min(py + fh, bh)
    if not ((-fw < px < bw) and (-fh < py < bh)): return back
    front3: np.ndarray = front[..., : 3]
    mask1: np.ndarray = front[..., 3]
    mask3: np.ndarray = cv2.merge((mask1, mask1, mask1))
    mask_roi: np.ndarray = mask3[sy - py: ey - py, sx - px: ex - px]
    front_roi: np.ndarray = front3[sy - py: ey - py, sx - px: ex - px]
    roi: np.ndarray = back[sy:ey, sx:ex]
    tmp1: np.ndarray = cv2.bitwise_and(roi, mask_roi)
    tmp2: np.ndarray = cv2.bitwise_or(tmp1, front_roi)
    back[sy:ey, sx:ex] = tmp2
    return back


FILE_PATH = 'src/video/'


def Edit(clip: int, textContent: str) -> None:
    """
    Edit Video
    --------------------------------

    Parameters:

               clip: int  - Twitch Clip ID
        textContent: str  - Text to display

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
    INPUT_VIDEO = cv2.VideoCapture(f'{FILE_PATH}download/{filename}')
    OUTPUT_VIDEO = cv2.VideoWriter(f'{FILE_PATH}export/{filename}', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 60, (1920, 1080))
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
    INPUT_VIDEO.release()
    OUTPUT_VIDEO.release()
    subprocess.call(f'ffmpeg -i {FILE_PATH}export/{filename} -i {FILE_PATH}download/{filename} -c:v copy {FILE_PATH}{filename} -loglevel quiet -y')


def main():
    Edit(991466429, 'Streamer Name')
    pass


if __name__ == '__main__': main()
