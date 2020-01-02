import random

from typing import Tuple
from typing import List
from typing import Generator
from typing import Optional

from PIL.Image import Image
from PIL.ImageDraw import Draw

from ..screens import BaseScreen


# =====
def circles(
    screen: BaseScreen,
    limit: Optional[int]=None,
    n: Tuple[int, int]=(3, 6),
    r: Tuple[int, int]=(5, 20),
    inc: Tuple[int, int]=(1, 2),
) -> Generator[Tuple[Image, Draw], None, None]:

    class Circle:
        def __init__(self) -> None:
            self.x = random.randint(0, screen.width)
            self.y = random.randint(0, screen.height)
            self.r = 0
            self.r_max = random.randint(*r)
            self.inc = random.randint(*inc)

    current: List[Circle] = []
    while True:
        n_cur = random.randint(*n)
        while len(current) < n_cur and (limit is None or limit > 0):
            current.append(Circle())

        if limit is not None:
            limit -= 1
            if len(current) == 0:
                yield screen.make_image()
                break

        (image, draw) = screen.make_image()
        for circle in list(current):
            draw.ellipse((
                circle.x - circle.r,
                circle.y - circle.r,
                circle.x + circle.r,
                circle.y + circle.r,
            ))
            circle.r += circle.inc
            if circle.r > circle.r_max:
                current.remove(circle)
        yield (image, draw)
