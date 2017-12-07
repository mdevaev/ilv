#!/usr/bin/env python3

from ilv import Screen
from ilv import Font
from ilv import make_image

from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image


#font = ImageFont.truetype('ilv/data/fonts/Lcd-2.ttf', 7)
#font = Font(["ilv/data/fonts/Lcd-2.ttf", "!ilv/data/fonts/Lcd-2.extra.yaml"])
#font = ImageFont.load_default()
#draw.polygon([(40,23), (50,2), (60,23)], outline=0, fill=255)
#draw.text((0,0), 'Привет, мир!\n   тест тест', font=font, fill=255)
#draw.text((0,0), '╔══════════════╗', font=font, fill=255)
#draw.multiline_text((0,8), 'a\nb', font=font, spacing=font.spacing, fill=255)
#draw.rectangle((0,0,94,22), outline=255)


#draw.bitmap((10,10), {(0,0):255, (0,1):255}, 255)
#image.show()


screen = Screen("/dev/ttyACM0")
screen.set_enabled(False)
screen.set_enabled()

import time, random, math

try:
    while True:
        """
        for i in range(47):
            (image, draw) = make_image()
            for _ in range(random.randint(int(95 * 23 * 0.3), int(95 * 23 * 0.6))):
                draw.point((
                    random.randint(0 + i, 95 - i),
                    random.randint(0, 23),
                ))
                draw.text((36, 8), "Тест")
            screen.send(image)
            time.sleep(0.01)
        time.sleep(3)
        """
        """
        (image, draw) = make_image()
        for _ in range(random.randint(int(95 * 23 * 0.3), int(95 * 23 * 0.6))):
            draw.point((
                random.randint(0, 95),
                random.randint(0, 23),
            ))
#            draw.text((36, 8), "Тест")
        screen.send(image)
        time.sleep(0.05)
        """
        """
        (image, draw) = make_image()
        draw.rectangle(((0, 0), (95, 23)), fill=255)
        screen.send(image)
        """
        x = random.randint(0, 95)
        y = random.randint(0, 23)
        m = random.randint(5, 20)
        for c in range(m):
            (image, draw) = make_image()
            draw.ellipse((x - c, y - c, x + c, y + c))
            screen.send(image)
            time.sleep(0.05)
        """
        for offset in range(30):
            xy = [
                (i - offset, (math.sin(i / 16. * math.pi) + 1) * 11)
                for i in range(offset, 95 + offset)
                ]
            (image, draw) = make_image()
            draw.point(xy)
            screen.send(image)
            time.sleep(0.01)
        """
except KeyboardInterrupt:
    screen.send(make_image()[0])



"""
draw.text((0, 0), "╔══════════════╗")
draw.text((0, 8), "║ Привет, мир! ║")
draw.text((0, 16),"╚══════════════╝")

screen.print(image)
screen.send(image)

s = " " * 16 + "Привет, мир!"
arr = []
for i in range(len(s)):
    image = Image.new('L', (95, 23), "black")
    draw = ImageDraw.Draw(image)
    draw.font = font
    draw.text((0, 8), s[i:i+16], fill=255)
    arr.append(screen.pack210(image))
#
import itertools, time
for a in itertools.cycle(arr):
    screen.send(a)
"""
