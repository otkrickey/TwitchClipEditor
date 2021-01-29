from typing import Tuple, Union

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class Rect:
    """
    長方形の画像の作成・出力

    Attributes
    ----------
    canvas : np.ndarray
        画像を作成するキャンバス

    size : Tuple[int, int]
        作成する画像のサイズ

    color : Tuple[int, int, int]
        作成する画像の色

    r : Union[int, float]
        角の丸み (0をしてすると直角)
    """

    def __init__(self, size: Tuple[int, int], color: Tuple[int, int, int], radius: Union[int, float]) -> None:
        """
        長方形の画像の作成

        Parameters
        ----------
        size : Tuple[int, int]
            作成する画像のサイズ

        color : Tuple[int, int, int]
            作成する画像の色

        r : Union[int, float]
            角の丸み (0をしてすると直角)
        """
        super().__init__()
        self.size = size
        self.color = color
        self.canvas: np.ndarray = np.full((size[1], size[0], 4), 0, dtype=np.uint8)
        cv2.rectangle(self.canvas, (radius, radius), (self.size[0] - radius, self.size[1] - radius), self.color, -1, cv2.LINE_AA)
        cv2.rectangle(self.canvas, (radius, radius), (self.size[0] - radius, self.size[1] - radius), self.color, radius * 2, cv2.LINE_AA)
        self.canvas[..., 3] = self.canvas[..., :3].sum(axis=2) / sum(self.color) * 255

    @property
    def image(self) -> np.ndarray:
        """
        長方形の画像の出力

        Returns
        -------
        canvas : np.ndarray
            作成された画像のコピーデータを出力。
        """
        return self.canvas.copy()


class Text:
    """
    文字の画像の作成・出力

    Attributes
    ----------
    canvas : np.ndarray
        画像を作成するキャンバス

    size : Tuple[int, int]
        作成する画像のサイズ

    color : Tuple[int, int, int]
        作成する画像の色

    content : str
        入力する文字

    fontsize : Union[int, float] = 36
        入力する文字サイズ
    """

    def __init__(self, size: Tuple[int, int], color: Tuple[int, int, int], content: str, fontsize: Union[int, float] = 36) -> None:
        """
        文字の画像の作成

        Parameters
        ----------
        size : Tuple[int, int]
            作成する画像のサイズ

        color : Tuple[int, int, int]
            作成する画像の色

        content : str
            入力する文字

        fontsize : Union[int, float]
            入力する文字サイズ
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
        文字の画像の出力

        Returns
        -------
        canvas : np.ndarray
            作成された画像のコピーデータを出力。
        """
        return self.canvas.copy()
