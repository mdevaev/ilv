import types

from typing import Tuple
from typing import List
from typing import IO
from typing import Type
from typing import Optional

import serial

from PIL.Image import new as make_new_image
from PIL.Image import Image

from PIL.ImageDraw import Draw

from ..fonts import get_default_font
from ..fonts import Font


# =====
# http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
_F_WHITE = "\033[37;1m"
_F_GRAY = "\033[38;5;236m"
_B_GRAY = "\033[48;5;236m"
_B_BLACK = "\033[40m"
_RESET = "\033[0m"

_BLOCKS = {
    (True, True): f"{_F_WHITE}█{_RESET}",
    (True, False): f"{_F_WHITE}{_B_GRAY}▀{_RESET}",
    (False, True): f"{_F_WHITE}{_B_GRAY}▄{_RESET}",
    (False, False): f"{_B_GRAY} {_RESET}",

    (True, None): f"{_F_WHITE}{_B_BLACK}▀{_RESET}",
    (None, True): f"{_F_WHITE}{_B_BLACK}▄{_RESET}",

    (False, None): f"{_F_GRAY}{_B_BLACK}▀{_RESET}",
    (None, False): f"{_F_GRAY}{_B_BLACK}▄{_RESET}",

    (None, None): f"{_B_BLACK} {_RESET}",
}


class _TermEcho:
    def __init__(self, screen: "BaseScreen", file: IO) -> None:
        if not file.isatty():
            raise RuntimeError(f"Echo file={file!r} is not a terminal")

        self.__screen = screen
        self.__file = file

        self.__printed = False

    def print(self, image: Image) -> None:
        width = self.__screen.width
        height = self.__screen.height
        b_width = self.__screen.block_width
        b_height = self.__screen.block_height

        pixels = image.load()
        rows: List[List[Optional[bool]]] = []
        for y in range(1, height + 1):
            if b_height == 0 or y % (b_height + 1) != 0:
                row: List[Optional[bool]] = []
                for x in range(1, width + 1):
                    if b_width == 0 or x % (b_width + 1) != 0:
                        row.append(bool(pixels[(x - 1, y - 1)]))
                    else:
                        row.append(None)
                rows.append(row)
            else:
                rows.append([None] * width)

        if self.__printed:
            self.__file.write(f"\033[{(height + 1) // 2}A")

        for y in range(0, len(rows), 2):
            for x in range(len(rows[y])):
                block_key = (
                    rows[y][x],  # Top
                    (rows[y + 1][x] if y + 1 < len(rows) else None),  # Bottom
                )
                self.__file.write(_BLOCKS[block_key])
            self.__file.write("\n")
            self.__file.flush()

        self.__printed = True


# =====
class BaseScreen:  # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        width: int,
        height: int,
        block_width: int,
        block_height: int,

        font: Optional[Font]=None,

        device_path: str="",
        device_speed: int=115200,

        echo_file: Optional[IO]=None,
    ) -> None:

        self.width = width
        self.height = height
        self.block_width = block_width
        self.block_height = block_height

        self.font = (font or get_default_font())

        self.__device_path = device_path
        self.__device_speed = device_speed

        self.__echo = (_TermEcho(self, echo_file) if echo_file else None)

        self.__tty: Optional[serial.Serial] = None

    def __enter__(self) -> "BaseScreen":
        if self.__device_path:
            self.__tty = serial.Serial(self.__device_path, self.__device_speed)
        return self

    def __exit__(
        self,
        _exc_type: Type[BaseException],
        _exc: BaseException,
        _tb: types.TracebackType,
    ) -> None:

        if self.__tty:
            self.__tty.close()

    # =====

    def make_image(
        self,
        image: Optional[Image]=None,
        font: Optional[Font]=None,
    ) -> Tuple[Image, Draw]:

        if image is not None:
            image = image.copy()
        else:
            image = make_new_image("L", (self.width, self.height), "black")

        draw = Draw(image)
        draw.font = (self.font or font)
        draw.ink = 255

        return (image, draw)

    def show(self, image: Image) -> None:
        if self.__tty:
            self.__send_image_data(self._pack_image(image))
        if self.__echo:
            self.__echo.print(image)

    def clear(self) -> None:
        self.show(self.make_image()[0])

    def set_enabled(self, enabled: bool=True) -> None:
        if self.__tty:
            if enabled:
                self.__tty.write(b"\x00\x01")
            else:
                self.__tty.write(b"\x00\x00")
            self.__tty.flush()

    # =====

    def _pack_image(self, image: Image) -> bytes:
        raise NotImplementedError

    def __send_image_data(self, data: bytes) -> None:
        assert self.__tty
        self.__tty.write(b"\x01")
        self.__tty.write(data)
        self.__tty.flush()
