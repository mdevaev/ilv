import sys

import serial


# =====
class Screen:
    def __init__(self, tty_path=None):
        self._tty = (serial.Serial(tty_path, 115200) if tty_path else None)
        self._screen = [[]]
        self.clear()

    def clear(self):
        self._screen = [[0] * 95 for _ in range(23)]

    def draw_pixel(self, x, y, bit=1):
        if 0 <= x < 95 and 0 <= y < 23:
            self._screen[y][x] = bit

    def draw_pixmap(self, x, y, pixmap):
        for (row_offset, row) in enumerate(pixmap, y):
            for (bit_offset, bit) in enumerate(row, x):
                self.draw_pixel(bit_offset, row_offset, bit)

    def draw_text(self, x, y, font, text):
        for (lineno, line) in enumerate(text.split("\n")):
            for (place, char) in enumerate(line):
                self.draw_pixmap(
                    x + place * font.width + place * font.spacing,
                    y + lineno * font.height + lineno * font.spacing,
                    font[char],
                )

    def print(self, file=sys.stdout):
        for (y, row) in enumerate(self._screen, 1):
            if y % 8:
                for (x, bit) in enumerate(row, 1):
                    if x % 6 == 0:
                        file.write(" ")
                    else:
                        file.write("\u2588" if bit else "_")
                file.write("\n")
            else:
                file.write("\n")

    def print_code(self, name="RENAME_ME", file=sys.stdout):
        data = [0] * 15 + self.pack105()
        print("const uint16_t %s[105] = {\n" % (name) + ",\n".join(
            "\t" + ",\t".join("0x%x" % (number) for number in row)
            for row in [data[index:index + 10] for index in range(0, len(data), 10)]
        ) + "\n};", file=file)

    def pack105(self):
        # 105 16-битных значений
        return [
            int("".join(map(str, row[x::6])), 2)
            for (y, row) in enumerate(self._screen)
            if y not in [7, 15, 23]
            for x in range(5)
        ]

    def pack210(self):
        # 210 8-битных парами старший-младший
        return [
            int("".join(map(str, row[part + x:part + 47:6])), 2)
            for (y, row) in enumerate(self._screen)
            if y not in [7, 15, 23]
            for x in range(5)
            for part in [0, 48]
        ]

    def send(self, data=None):
        assert data is None or len(data) == 210
        if self._tty:
            self._tty.write(b"\x01")
            self._tty.write(bytes(self.pack210() if data is None else data))
            self._tty.flush()

    def set_enabled(self, enabled=True):
        if self._tty:
            if enabled:
                self._tty.write(b"\x00\x01")
                self.send()
            else:
                self._tty.write(b"\x00\x00")
                self.send([0] * 210)
