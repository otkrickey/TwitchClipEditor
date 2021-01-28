from typing import Tuple
from src.python.createImage import Rect, Text
import numpy as np
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

