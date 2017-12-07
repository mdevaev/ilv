from fontTools.ttLib import TTFont

from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image

import yaml


# =====
class Font:
    def __init__(self, paths, width=5, height=7, spacing=1):
        self.width = width
        self.height = height
        self.spacing = spacing

        self._fallback_char = [
            [
                (1 if y in [0, height - 1] or x in [0, width - 1] else 0)
                for x in range(width)
            ]
            for y in range(height)
        ]

        self._font = {}
        for path in paths:
            if path.lower().endswith(".yaml"):
                reader = self._read_yaml_font
            elif path.lower().endswith(".ttf"):
                reader = self._read_ttf_font
            else:
                raise RuntimeError("Invalid font type: %s" % (path))
            ignore = self._font
            if path.startswith("!"):
                path = path[1:]
                ignore = None
            self._font.update(reader(path, ignore=ignore))

    def __getitem__(self, key):
        return self._font.get(key, self._fallback_char)

    def _read_yaml_font(self, path, ignore):
        with open(path) as font_file:
            return {
                chr(char): [
                    [
                        (1 if pixel == "X" else 0)
                        for pixel in str(row)
                    ]
                    for row in pixmap
                ]
                for (char, pixmap) in yaml.load(font_file).items()
                if not ignore or char not in ignore
            }

    def _read_ttf_font(self, path, ignore):
        image_font = ImageFont.truetype(path, self.height)
        return {
            char: self._render_image_char(image_font, char)
            for char in self._get_ttf_chars(path)
            if not ignore or char not in ignore
        }

    def _get_ttf_chars(self, path):
        return set(
            chr(code)
            for table in TTFont(path)["cmap"].tables
            for code in table.cmap
        )

    def _render_image_char(self, image_font, char):
        image = Image.new("RGB", (self.width, self.height), "black")
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), char, font=image_font)
        image = image.convert("L")
        pixels = image.load()
        return [
            [
                int(bool(pixels[x,y]))
                for x in range(self.width)
            ]
            for y in range(self.height)
        ]
