from typing import Tuple, Union

import cv2
import numpy as np
from matplotlib import pyplot as plt
from src.python.createImage import Rect, Text
from src.python.easing import Easing


class Image:
    def __init__(self, image: np.ndarray, timing: Tuple[int, int], start_position: Tuple(int, int), end_position: Tuple(int, int)) -> None:
        self.image = image
        self.st = timing[0]
        self.et = timing[1]
        self.spx = start_position[0]
        self.spy = start_position[1]
        self.epx = end_position[0]
        self.epy = end_position[1]

    def position(self, t) -> Tuple[int, int]:
        if t < self.st:
            return (self.spx, self.spy)
        elif self.st <= t < self.et:
            return (int(self.spx if self.spx == self.epx else Easing((t - self.st) / (self.et - self.st)).easeInOutBack * (self.epx - self.spx) + self.spx),
                    int(self.spy if self.spy == self.epy else Easing((t - self.st) / (self.et - self.st)).easeInOutBack * (self.epy - self.spy) + self.spy))
        else:
            return (self.epx, self.epy)


def mask(back: np.ndarray, front: np.ndarray, position: Tuple[int, int]) -> np.ndarray:
    """
    `back`に指定された画像に`front`に指定した画像を`position`で指定した位置に合成する。

    Parameters
    ----------
    back : np.ndarray
        背景画像。後ろ側の画像。
    front : np.ndarray
        合成画像。手間側の画像。
    position : Tuple[int, int]
        合成する位置。`back`に指定した画像の左上を基準に横軸x、縦軸yで指定する。
        `front`に指定した画像の左上の場所を指す。

    Returns
    -------
    back : np.ndarray
        合成後の背景画像。
    """
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
    mask3: np.ndarray = cv2.merge(mask1, mask1, mask1)
    mask_roi: np.ndarray = mask3[py1 - py: py2 - py, px1 - px: px2 - px]
    front_roi: np.ndarray = front3[py1 - py: py2 - py, px1 - px: px2 - px]
    roi: np.ndarray = back[py1:py2, px1:px2]
    tmp1: np.ndarray = cv2.bitwise_and(roi, mask_roi)
    tmp2: np.ndarray = cv2.bitwise_or(tmp1, front_roi)
    back[py1:py2, px1:px2] = tmp2
    return back
