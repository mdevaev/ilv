#!/usr/bin/env python3

from ilv import Screen
from ilv import Font


# https://fontstruct.com/gallery/tag/386/5x7
font = Font(["ilv/data/fonts/Lcd-2.ttf", "!ilv/data/fonts/Lcd-2.extra.yaml"])

screen = Screen("/dev/ttyACM0")
#screen.draw_text(0, 0, font,  "╔══════════════╗")
#screen.draw_text(0, 8, font, "║ Привет, мир! ║")
#screen.draw_text(0, 16, font,  "╚══════════════╝")
#screen.draw_line(5, 5, 20, 20)
#screen.draw_circle(10, 10, 7)
#screen.draw_text(24, 8, font, "Загрузка")
#screen.draw_text(0, 0, font, "Вконтач:   15330\nАкомикс:    1963\nТапастик:   1829")

#import math
#for x in range(95):
#    y = abs(int(math.sin(x / 5) * 10 - 12))
#    screen.draw_pixel(x, y)

#screen.print_code()
for x in range(95):
    for y in range(23):
        screen.draw_pixel(x, y)
#screen.print()
#screen.send()
screen.set_enabled(1)
#import time
#time.sleep(5)
#screen.set_enabled(0)
#time.sleep(5)
#screen.set_enabled(1)
#while True:
#    screen.draw_text(0, 0, font,  "╔══════════════╗")
#    screen.draw_text(0, 8, font, "║ Привет, мир! ║")
#    screen.draw_text(0, 16, font,  "╚══════════════╝")
#    screen.send()
#    screen.clear()

"""
s = " " * 16 + "Привет, мир!"
arr = []
for i in range(len(s)):
    screen.draw_text(0, 8, font, s[i:i+16])
    arr.append(screen.pack210())
    screen.clear()
#
import itertools, time
for a in itertools.cycle(arr):
    screen.send(a)
"""
