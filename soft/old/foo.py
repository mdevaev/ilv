#!/usr/bin/env python3

from ilv import Screen
from ilv import Font

from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image


font = ImageFont.truetype('ilv/data/fonts/Lcd-2.ttf', 7)
#font = ImageFont.load_default()
image = Image.new('1', (95, 23))
draw = ImageDraw.Draw(image)
#draw.rectangle((0,0,94,22), outline=255, fill=0)
#draw.polygon([(40,23), (50,2), (60,23)], outline=0, fill=255)
#draw.text((0,0), 'Привет, мир!\nТест', font=font, fill=255, features=["vkrn"])
draw.bitmap((10,10), {(0,0):255, (0,1):255}, 255)

screen = Screen()#"/dev/ttyACM0")
pix = image.load()
for y in range(23):
    for x in range(95):
        screen._screen[y][x] = bool(pix[(x, y)])

screen.print()
