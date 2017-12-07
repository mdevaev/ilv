import sys

import serial

from PIL import Image
from PIL import ImageDraw

from ..font import get_default_font


# =====
class BaseScreen:
    WIDTH = None
    HEIGHT = None
    PACK_SIZE = None

    def __init__(self, tty_path=None, default_font=None):
        assert self.WIDTH
        assert self.HEIGHT
        assert self.PACK_SIZE
        self._tty = (serial.Serial(tty_path, 115200) if tty_path else None)
        self.default_font = (default_font or get_default_font())

    def make_image(self, image=None, default_font=None):
        if image:
            image = image.copy()
        else:
            image = Image.new("L", (self.WIDTH, self.HEIGHT), "black")
        draw = ImageDraw.Draw(image)
        draw.font = (self.default_font or default_font)
        draw.ink = 255
        return (image, draw)

    def print(self, image, file=sys.stdout):
        raise NotImplementedError

    def pack(self, image):
        raise NotImplementedError

    def send(self, image):
        if self._tty:
            if isinstance(image, bytes):
                data = image
            else:
                data = self.pack(image)
            assert len(data) == self.PACK_SIZE
            self._tty.write(b"\x01")
            self._tty.write(data)
            self._tty.flush()

    def clear(self):
        self.send(b"\x00" * self.PACK_SIZE)

    def set_enabled(self, enabled=True):
        if self._tty:
            if enabled:
                self._tty.write(b"\x00\x01")
            else:
                self._tty.write(b"\x00\x00")
                self.clear()
