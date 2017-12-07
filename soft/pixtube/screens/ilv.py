import sys

from . import BaseScreen


# =====
class Screen(BaseScreen):
    WIDTH = 95
    HEIGHT = 23
    PACK_SIZE = 210

    def print(self, image, file=sys.stdout):
        pixels = image.load()
        for y in range(1, 24):
            if y % 8:
                for x in range(1, 96):
                    if x % 6 == 0:
                        file.write(" ")
                    else:
                        file.write("\u2588" if pixels[(x - 1, y - 1)] else "_")
                file.write("\n")
            else:
                file.write("\n")

    def pack(self, image):
        # 210 8-битных парами старший-младший
        # Метод упаковки:
        # x**** x**** ...
        # *x*** *x*** ...
        # Первый байт отвечает за левую половину экрана, второй - за правую.
        pixels = image.load()
        return bytes(
            int("".join(map(
                lambda x: ("1" if pixels[(x, y)] else "0"),
                range(x_part + x_start, x_part + 47, 6),
            )), 2)
            for y in range(23)
            if y not in [7, 15, 23]
            for x_start in range(5)
            for x_part in [0, 48]
        )
