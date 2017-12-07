import random


# =====
def random_fill(screen, image, n=(5, 15)):
    yield from _filled_by_pixels(*screen.make_image(), _get_white_pixels(image), n, 255)


def random_unfill(screen, image, n=(5, 15)):
    yield from _filled_by_pixels(*screen.make_image(image), _get_white_pixels(image), n, 0)


def _get_white_pixels(image):
    pixels = image.load()
    return set(
        (x, y)
        for x in range(image.width)
        for y in range(image.height)
        if pixels[(x, y)]
    )


def _filled_by_pixels(image, draw, pixels, n, fill):
    while len(pixels):
        for pixel in random.sample(pixels, min(len(pixels), random.randint(*n))):
            draw.point(pixel, fill=fill)
            pixels.remove(pixel)
        yield (image, draw)
