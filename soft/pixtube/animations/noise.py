import random

from typing import Tuple
from typing import Generator
from typing import Optional

from PIL.Image import Image
from PIL.ImageDraw import Draw

from ..screens import BaseScreen


# =====
def white_noise(
    screen: BaseScreen,
    limit: Optional[int]=None,
) -> Generator[Tuple[Image, Draw], None, None]:

    while limit is None or limit > 0:
        (image, draw) = screen.make_image()
        image.putdata(list(map(
            (lambda _: random.randint(0, 1)),
            [0] * screen.width * screen.height,
        )))
        if limit:
            limit -= 1
        yield (image, draw)
