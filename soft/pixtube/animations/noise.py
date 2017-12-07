import random


# =====
def white_noise(screen, limit=None):
    while limit is None or limit > 0:
        (image, draw) = screen.make_image()
        image.putdata(list(map(
            lambda _: random.randint(0, 1),
            [0] * screen.WIDTH * screen.HEIGHT,
        )))
        yield (image, draw)
        limit -= 1
