import sys
import os
import functools

from fontTools.ttLib import TTFont

from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image

import yaml


# =====
@functools.lru_cache()
def get_default_font():
    return Font([
        os.path.join(os.path.dirname(sys.modules["pixtube"].__file__), "data/fonts", name)
        for name in ["Lcd-2.ttf", "Lcd-2.extra.yaml"]
    ])


class Font:
    def __init__(self, paths, width=5, height=7, spacing=1):
        self.paths = paths
        self.width = width
        self.height = height
        self.spacing = spacing

        self._fallback_letter = self._make_fallback_letter()
        self._font = self._build_font()

    def getsize(self, text, *args, **kwargs):
        rows = text.split("\n")
        nrows = len(rows)
        nchars = max(map(len, rows))
        return (
            (nchars * self.width + (nchars - 1) * self.spacing),
            (nrows * self.height + (nrows - 1) * self.spacing),
        )

    def getmask(self, text, *args, **kwargs):
        image = Image.new("L", self.getsize(text), "black")
        draw = ImageDraw.Draw(image)
        (x, y) = (0, 0)
        for row in text.split("\n"):
            for char in row:
                draw.bitmap((x, y), self._font.get(char, self._fallback_letter), fill=255)
                x += self.width + self.spacing
            x = 0
            y += self.height + self.spacing
        return image.im

    # =====

    def _make_fallback_letter(self):
        image = Image.new("L", (self.width, self.height), "black")
        draw = ImageDraw.Draw(image)
        draw.point([
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if y in [0, self.height - 1] or x in [0, self.width - 1]
        ], fill=255)

    def _build_font(self):
        font = {}
        for path in self.paths:
            if path.lower().endswith(".yaml"):
                reader = self._read_yaml_font
            elif path.lower().endswith(".ttf"):
                reader = self._read_ttf_font
            else:
                raise RuntimeError("Invalid font type: %s" % (path))
            ignore = font
            if path.startswith("!"):
                path = path[1:]
                ignore = None
            font.update(reader(path, ignore=ignore))
        return font

    def _read_yaml_font(self, path, ignore):
        with open(path) as font_file:
            font = {}
            for (char, pixmap) in yaml.load(font_file).items():
                if not ignore or char not in ignore:
                    image = Image.new("L", (self.width, self.height), "black")
                    draw = ImageDraw.Draw(image)
                    draw.point([
                        (x, y)
                        for (y, row) in enumerate(pixmap)
                        for (x, pixel) in enumerate(str(row))
                        if pixel == "X"
                    ], fill=255)
                    font[chr(char)] = image
            return font

    def _read_ttf_font(self, path, ignore):
        font = {}
        image_font = ImageFont.truetype(path, self.height)
        for table in TTFont(path)["cmap"].tables:
            for char in map(chr, table.cmap):
                if not ignore or char not in ignore:
                    image = Image.new("L", (self.width, self.height), "black")
                    draw = ImageDraw.Draw(image)
                    draw.text((0, 0), char, font=image_font, fill=255)
                    font[char] = image
        return font
