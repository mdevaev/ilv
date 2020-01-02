import sys
import os
import functools

from typing import Tuple
from typing import List
from typing import Dict
from typing import Set
from typing import NewType
from typing import Any

from fontTools.ttLib import TTFont

from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image

import yaml


# =====
@functools.lru_cache()
def get_default_font() -> "Font":
    return Font([
        os.path.join(os.path.dirname(sys.modules[__name__].__file__), "data", name)
        for name in ["Lcd-2.ttf", "Lcd-2.extra.yaml"]
    ])


# =====
_IM = NewType("_IM", int)  # FIXME: A stub for the internal type in C binding


class Font:
    def __init__(
        self,
        paths: List[str],
        width: int=5,
        height: int=7,
        spacing: int=1,
    ) -> None:

        self.__paths = paths

        self.width = width
        self.height = height
        self.spacing = spacing

        self.__fallback_letter = self.__make_fallback_letter()
        self.__font = self.__build_font()

    # ===== Мимикрируем под PIL API

    def getsize(self, text: str, *_: Any, **__: Any) -> Tuple[int, int]:
        rows = text.split("\n")
        n_rows = len(rows)
        n_chars = max(map(len, rows))
        return (
            (n_chars * self.width + (n_chars - 1) * self.spacing),
            (n_rows * self.height + (n_rows - 1) * self.spacing),
        )

    def getmask(self, text: str, *_: Any, **__: Any) -> _IM:
        image = Image.new("L", self.getsize(text), "black")
        draw = ImageDraw.Draw(image)
        (x, y) = (0, 0)
        for row in text.split("\n"):
            for char in row:
                draw.bitmap((x, y), self.__font.get(char, self.__fallback_letter), fill=255)
                x += self.width + self.spacing
            x = 0
            y += self.height + self.spacing
        return image.im

    # =====

    def __make_fallback_letter(self) -> _IM:
        image = Image.new("L", (self.width, self.height), "black")
        draw = ImageDraw.Draw(image)
        draw.point([
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if y in [0, self.height - 1] or x in [0, self.width - 1]
        ], fill=255)
        return image

    def __build_font(self) -> Dict[str, _IM]:
        font: Dict[str, _IM] = {}
        for path in self.__paths:
            if path.lower().endswith(".yaml"):
                reader = self.__read_yaml_font
            elif path.lower().endswith(".ttf"):
                reader = self.__read_ttf_font
            else:
                raise RuntimeError(f"Invalid font type: {path}")
            ignore: Set[str] = set(font)
            if path.startswith("!"):
                path = path[1:]
                ignore = set()
            font.update(reader(path, ignore=ignore))
        return font

    def __read_yaml_font(self, path: str, ignore: Set[str]) -> Dict[str, _IM]:
        with open(path) as font_file:
            font: Dict[str, _IM] = {}
            for (char, pixmap) in yaml.safe_load(font_file).items():
                if char not in ignore:
                    image = Image.new("L", (self.width, self.height), "black")
                    draw = ImageDraw.Draw(image)
                    draw.point([
                        (x, y)
                        for (y, row) in enumerate(pixmap)
                        for (x, pixel) in enumerate(str(row).replace(" ", ""))
                        if pixel != "."
                    ], fill=255)
                    font[chr(char)] = image
            return font

    def __read_ttf_font(self, path: str, ignore: Set[str]) -> Dict[str, _IM]:
        font: Dict[str, _IM] = {}
        image_font = ImageFont.truetype(path, self.height)
        for table in TTFont(path)["cmap"].tables:
            for char in map(chr, table.cmap):
                if char not in ignore:
                    image = Image.new("L", (self.width, self.height), "black")
                    draw = ImageDraw.Draw(image)
                    draw.text((0, 0), char, font=image_font, fill=255)
                    font[char] = image
        return font
