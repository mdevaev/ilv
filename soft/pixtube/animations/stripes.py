import random


# =====
def hor_stripes_fill(screen, image):
    (left, draw) = screen.make_image(image)
    for y in range(1, screen.HEIGHT, 2):
        draw.line((0, y, screen.WIDTH, y), fill=0)

    (right, draw) = screen.make_image(image)
    for y in range(0, screen.HEIGHT, 2):
        draw.line((0, y, screen.WIDTH, y), fill=0)

    for offset in range(screen.WIDTH):
        (image, draw) = screen.make_image()
        image.paste(left, (offset - screen.WIDTH + 1, 0))
        image.paste(right, (screen.WIDTH - offset - 1, 0), right)
        yield (image, draw)


def hor_stripes_unfill(screen, image):
    (left, draw) = screen.make_image(image)
    for y in range(1, screen.HEIGHT, 2):
        draw.line((0, y, screen.WIDTH, y), fill=0)

    (right, draw) = screen.make_image(image)
    for y in range(0, screen.HEIGHT, 2):
        draw.line((0, y, screen.WIDTH, y), fill=0)

    for offset in range(screen.WIDTH):
        (image, draw) = screen.make_image()
        image.paste(left, (-offset - 1, 0))
        image.paste(right, (offset + 1, 0), right)
        yield (image, draw)


def vert_stripes_fill(screen, image):
    (up, draw) = screen.make_image(image)
    for x in range(1, screen.WIDTH, 2):
        draw.line((x, 0, x, screen.HEIGHT), fill=0)

    (down, draw) = screen.make_image(image)
    for x in range(0, screen.WIDTH, 2):
        draw.line((x, 0, x, screen.HEIGHT), fill=0)

    for offset in range(screen.HEIGHT):
        (image, draw) = screen.make_image()
        image.paste(up, (0, offset - screen.HEIGHT + 1))
        image.paste(down, (0, screen.HEIGHT - offset - 1), down)
        yield (image, draw)


def vert_stripes_unfill(screen, image):
    (up, draw) = screen.make_image(image)
    for x in range(1, screen.WIDTH, 2):
        draw.line((x, 0, x, screen.HEIGHT), fill=0)

    (down, draw) = screen.make_image(image)
    for x in range(0, screen.WIDTH, 2):
        draw.line((x, 0, x, screen.HEIGHT), fill=0)

    for offset in range(screen.HEIGHT):
        (image, draw) = screen.make_image()
        image.paste(up, (0, -offset - 1))
        image.paste(down, (0, offset + 1), down)
        yield (image, draw)
