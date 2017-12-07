import random


# =====
def circles(screen, limit=None, n=(3, 6), r=(5, 20), inc=(1, 2)):
    class Circle:
        def __init__(self):
            self.x = random.randint(0, screen.WIDTH)
            self.y = random.randint(0, screen.HEIGHT)
            self.r = 0
            self.r_max = random.randint(*r)
            self.inc = random.randint(*inc)

    circles = []
    while True:
        n_cur = random.randint(*n)
        while len(circles) < n_cur and (limit is None or limit > 0):
            circles.append(Circle())

        if limit is not None:
            limit -= 1
            if len(circles) == 0:
                yield screen.make_image()
                break

        (image, draw) = screen.make_image()
        for circle in list(circles):
            draw.ellipse((
                circle.x - circle.r,
                circle.y - circle.r,
                circle.x + circle.r,
                circle.y + circle.r,
            ))
            circle.r += circle.inc
            if circle.r > circle.r_max:
                circles.remove(circle)
        yield (image, draw)
