import math
import subprocess
from typing import Tuple, Union

import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont


class Easing:
    """
    Easing Functions
    ------

    Methods:

                      In: float  -     In ShortCut Function
                     Out: float  -    Out ShortCut Function
                   InOut: float  -  InOut ShortCut Function
                  Bounce: float  - Bounce ShortCut Function

              easeInSine: float  - easeInSine
             easeOutSine: float  - easeOutSine
           easeInOutSine: float  - easeInOutSine

              easeInQuad: float  - easeInQuad
             easeOutQuad: float  - easeOutQuad
           easeInOutQuad: float  - easeInOutQuad

             easeInCubic: float  - easeInCubic
            easeOutCubic: float  - easeOutCubic
          easeInOutCubic: float  - easeInOutCubic

             easeInQuart: float  - easeInQuart
            easeOutQuart: float  - easeOutQuart
          easeInOutQuart: float  - easeInOutQuart

             easeInQuint: float  - easeInQuint
            easeOutQuint: float  - easeOutQuint
          easeInOutQuint: float  - easeInOutQuint

              easeInExpo: float  - easeInExpo
             easeOutExpo: float  - easeOutExpo
           easeInOutExpo: float  - easeInOutExpo

              easeInCirc: float  - easeInCirc
             easeOutCirc: float  - easeOutCirc
           easeInOutCirc: float  - easeInOutCirc

              easeInBack: float  - easeInBack
             easeOutBack: float  - easeOutBack
           easeInOutBack: float  - easeInOutBack

           easeInElastic: float  - easeInElastic
          easeOutElastic: float  - easeOutElastic
        easeInOutElastic: float  - easeInOutElastic

            easeInBounce: float  - easeInBounce
           easeOutBounce: float  - easeOutBounce
         easeInOutBounce: float  - easeInOutBounce
    """

    def __init__(self, x: float) -> None: self.x = x
    def In(self, i: int) -> float: return self.x ** i
    def Out(self, i: int) -> float: return 1 - (1 - self.x) ** i
    def InOut(self, i: int) -> float: return 2 ** (i - 1) * self.x ** i if self.x < 0.5 else 1 - 2 ** (i - 1) * (1 - self.x) ** i
    def Bounce(self, t: int) -> float: return 7.5625 * t ** 2 if (t < 1 / 2.75) else 7.5625 * (t - 1.5 / 2.75) ** 2 + 0.75 if (t < 2 / 2.75) else 7.5625 * (t - 2.25 / 2.75) ** 2 + 0.9375 if (t < 2.5 / 2.75) else 7.5625 * (t - 2.625 / 2.75) ** 2 + 0.984375
    @property
    def easeInSine(self) -> float: return 1 - math.cos((self.x * math.pi) / 2)
    @property
    def easeOutSine(self) -> float: return math.sin((self.x * math.pi) / 2)
    @property
    def easeInOutSine(self) -> float: return -(math.cos(self.x * math.pi) - 1) / 2
    @property
    def easeInQuad(self) -> float: return self.In(2)
    @property
    def easeOutQuad(self) -> float: return self.Out(2)
    @property
    def easeInOutQuad(self) -> float: return self.InOut(2)
    @property
    def easeInCubic(self) -> float: return self.In(3)
    @property
    def easeOutCubic(self) -> float: return self.Out(3)
    @property
    def easeInOutCubic(self) -> float: return self.InOut(3)
    @property
    def easeInQuart(self) -> float: return self.In(4)
    @property
    def easeOutQuart(self) -> float: return self.Out(4)
    @property
    def easeInOutQuart(self) -> float: return self.InOut(4)
    @property
    def easeInQuint(self) -> float: return self.In(5)
    @property
    def easeOutQuint(self) -> float: return self.Out(5)
    @property
    def easeInOutQuint(self) -> float: return self.InOut(5)
    @property
    def easeInExpo(self) -> float: return 0 if self.x == 0 else 2 ** (10 * self.x - 10)
    @property
    def easeOutExpo(self) -> float: return 1 if self.x == 1 else 1 - 2 ** (-10 * self.x)
    @property
    def easeInOutExpo(self) -> float: return 0 if self.x == 0 else 1 if self.x == 1 else 2 ** (20 * self.x - 11) if self.x < 0.5 else 1 - 2 ** (-20 * self.x + 9)
    @property
    def easeInCirc(self) -> float: return 1 - math.sqrt(1 - self.x ** 2)
    @property
    def easeOutCirc(self) -> float: return 1 - math.sqrt(1 - (1 - self.x) ** 2)
    @property
    def easeInOutCirc(self) -> float: return (1 + math.sqrt(1 - 4 * (self.x if self.x < 0.5 else (1 - self.x)) ** 2)) / 2
    @property
    def easeInBack(self) -> float: return (2.70158 * self.x - 1.70158) * self.x ** 2
    @property
    def easeOutBack(self) -> float: return 1 + (2.70158 * self.x - 1) * (1 - self.x) ** 2
    @property
    def easeInOutBack(self) -> float: return 2 * self.x ** 2 * (3.59491 * 2 * self.x - 2.59491) if self.x < 0.5 else 2 * (1 - self.x) ** 2 * (7.18982 * self.x - 4.59491) + 1
    @property
    def easeInElastic(self) -> float: return 0 if self.x == 0 else 1 if self.x == 1 else -2 ** (10 * self.x - 10) * math.sin((self.x * 10 - 10.75) * math.pi * 1.5)
    @property
    def easeOutElastic(self) -> float: return 0 if self.x == 0 else 1 if self.x == 1 else 2 ** (-10 * self.x) * math.sin((self.x * 10 - 0.75) * math.pi * 1.5) + 1
    @property
    def easeInOutElastic(self) -> float: return 0 if self.x == 0 else 1 if self.x == 1 else -2 ** (20 * self.x - 11) * math.sin((20 * self.x - 11.125) * math.pi * 2.25) if self.x < 0.5 else 2 ** (-20 * self.x + 9) * math.sin((20 * self.x - 11.125) * math.pi * 2.25) + 1
    @property
    def easeInBounce(self) -> float: return 1 - self.Bounce(1 - self.x)
    @property
    def easeOutBounce(self) -> float: return self.Bounce(self.x)
    @property
    def easeInOutBounce(self) -> float: return (1 - self.Bounce(1 - 2 * self.x)) / 2 if self.x < 0.5 else (1 + self.Bounce(2 * self.x - 1)) / 2


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
    mask3: np.ndarray = 255 - cv2.merge((mask1, mask1, mask1))
    mask_roi: np.ndarray = mask3[sy - py: ey - py, sx - px: ex - px]
    front_roi: np.ndarray = front3[sy - py: ey - py, sx - px: ex - px]
    roi: np.ndarray = back[sy:ey, sx:ex]
    tmp1: np.ndarray = cv2.bitwise_and(roi, mask_roi)
    tmp2: np.ndarray = cv2.bitwise_or(tmp1, front_roi)
    back[sy:ey, sx:ex] = tmp2
    return back


FILE_PATH = 'src/video/'


def Edit(clip: int, textContent: str, callback: callable = None) -> None:
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
        if callback: callback(i)
    INPUT_VIDEO.release()
    OUTPUT_VIDEO.release()
    subprocess.call(f'ffmpeg -i {FILE_PATH}export/{filename} -i {FILE_PATH}download/{filename} -c:v copy {FILE_PATH}{filename} -loglevel quiet -y')


def main():
    Edit(991466429, 'Streamer Name')
    pass


if __name__ == '__main__': main()
