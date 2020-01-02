import random

from typing import Tuple
from typing import Set
from typing import Generator

from PIL.Image import Image
from PIL.ImageDraw import Draw

from ..screens import BaseScreen


# =====
def random_fill(
    screen: BaseScreen,
    image: Image,
    n: Tuple[int, int]=(5, 15),
) -> Generator[Tuple[Image, Draw], None, None]:

    yield from _filled_by_pixels(*screen.make_image(), _get_white_pixels(image), n, True)


def random_unfill(
    screen: BaseScreen,
    image: Image,
    n: Tuple[int, int]=(5, 15),
) -> Generator[Tuple[Image, Draw], None, None]:

    yield from _filled_by_pixels(*screen.make_image(image), _get_white_pixels(image), n, False)


def _get_white_pixels(image: Image) -> Set[Tuple[int, int]]:
    pixels = image.load()
    return set(
        (x, y)
        for x in range(image.width)
        for y in range(image.height)
        if pixels[(x, y)]
    )


def _filled_by_pixels(
    image: Image,
    draw: Draw,
    pixels: Set[Tuple[int, int]],
    n: Tuple[int, int],
    fill: bool,
) -> Generator[Tuple[Image, Draw], None, None]:

    while len(pixels):
        for pixel in random.sample(pixels, min(len(pixels), random.randint(*n))):
            draw.point(pixel, fill=(255 if fill else 0))
            pixels.remove(pixel)
        yield (image, draw)
