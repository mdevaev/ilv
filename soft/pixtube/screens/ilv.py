from typing import Any

from PIL.Image import Image

from . import BaseScreen


# =====
class Screen(BaseScreen):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            width=95,
            height=23,
            block_width=5,
            block_height=7,
            **kwargs,
        )

    def _pack_image(self, image: Image) -> bytes:
        # 210 8-битных парами старший-младший
        # Метод упаковки:
        #           старший         младший
        #   байт 1: x**** x**** ... x**** x****
        #   байт 2: *x*** *x*** ... *x*** *x***
        #
        # Первый байт отвечает за левую половину экрана, второй - за правую.
        pixels = image.load()
        return bytes(
            int("".join(map(
                (lambda x: ("1" if pixels[(x, y)] else "0")),  # pylint: disable=cell-var-from-loop
                range(x_part + x_start, x_part + 47, 6),
            )), 2)
            for y in range(23)
            if y not in [7, 15, 23]
            for x_start in range(5)
            for x_part in [0, 48]
        )
