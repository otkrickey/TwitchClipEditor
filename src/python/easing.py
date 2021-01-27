import math


class Easing:
    def __init__(self, x) -> None:
        super().__init__()
        self.x = x

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
