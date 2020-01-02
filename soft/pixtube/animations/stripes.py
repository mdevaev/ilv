from typing import Tuple
from typing import Generator

from PIL.Image import Image
from PIL.ImageDraw import Draw

from ..screens import BaseScreen


# =====
def hor_stripes_fill(screen: BaseScreen, image: Image) -> Generator[Tuple[Image, Draw], None, None]:
    (left, draw) = screen.make_image(image)
    for y in range(1, screen.height, 2):
        draw.line((0, y, screen.width, y), fill=0)

    (right, draw) = screen.make_image(image)
    for y in range(0, screen.height, 2):
        draw.line((0, y, screen.width, y), fill=0)

    for offset in range(screen.width):
        (image, draw) = screen.make_image()
        image.paste(left, (offset - screen.width + 1, 0))
        image.paste(right, (screen.width - offset - 1, 0), right)
        yield (image, draw)


def hor_stripes_unfill(screen: BaseScreen, image: Image) -> Generator[Tuple[Image, Draw], None, None]:
    (left, draw) = screen.make_image(image)
    for y in range(1, screen.height, 2):
        draw.line((0, y, screen.width, y), fill=0)

    (right, draw) = screen.make_image(image)
    for y in range(0, screen.height, 2):
        draw.line((0, y, screen.width, y), fill=0)

    for offset in range(screen.width):
        (image, draw) = screen.make_image()
        image.paste(left, (-offset - 1, 0))
        image.paste(right, (offset + 1, 0), right)
        yield (image, draw)


def vert_stripes_fill(screen: BaseScreen, image: Image) -> Generator[Tuple[Image, Draw], None, None]:
    (up, draw) = screen.make_image(image)
    for x in range(1, screen.width, 2):
        draw.line((x, 0, x, screen.height), fill=0)

    (down, draw) = screen.make_image(image)
    for x in range(0, screen.width, 2):
        draw.line((x, 0, x, screen.height), fill=0)

    for offset in range(screen.height):
        (image, draw) = screen.make_image()
        image.paste(up, (0, offset - screen.height + 1))
        image.paste(down, (0, screen.height - offset - 1), down)
        yield (image, draw)


def vert_stripes_unfill(screen: BaseScreen, image: Image) -> Generator[Tuple[Image, Draw], None, None]:
    (up, draw) = screen.make_image(image)
    for x in range(1, screen.width, 2):
        draw.line((x, 0, x, screen.height), fill=0)

    (down, draw) = screen.make_image(image)
    for x in range(0, screen.width, 2):
        draw.line((x, 0, x, screen.height), fill=0)

    for offset in range(screen.height):
        (image, draw) = screen.make_image()
        image.paste(up, (0, -offset - 1))
        image.paste(down, (0, offset + 1), down)
        yield (image, draw)
