#!/usr/bin/env python3

from pixtube.screens.ilv import Screen
from pixtube.animations.circles import circles
from pixtube.animations.noise import white_noise
from pixtube.animations.filler import random_fill
from pixtube.animations.filler import random_unfill
from pixtube.animations.stripes import hor_stripes_fill
from pixtube.animations.stripes import hor_stripes_unfill
from pixtube.animations.stripes import vert_stripes_fill
from pixtube.animations.stripes import vert_stripes_unfill
import time

screen = Screen("/dev/ttyACM0")
screen.set_enabled()

try:
    for (image, draw) in white_noise(screen, 500):
        screen.send(image)

    (image, draw) = screen.make_image()
    draw.text((18, 8), "Привет ^_^")

    for (image, draw) in random_fill(screen, image):
        screen.send(image)
        time.sleep(0.05)
    time.sleep(4)
    for (image, draw) in random_unfill(screen, image):
        screen.send(image)
        time.sleep(0.05)

    draw.text((0, 0), "Я экран из лампы")
    draw.text((0, 16), "  ИЛВ1-48/5*7")

    for (image, draw) in vert_stripes_fill(screen, image):
        screen.send(image)
        time.sleep(0.01)
    time.sleep(4)
    for (image, draw) in hor_stripes_unfill(screen, image):
        screen.send(image)
        time.sleep(0.01)
    time.sleep(1)

    draw.text((0, 0), "У меня внутри")
    draw.text((0, 8), "ардуина, max6921")
    draw.text((0, 16), "пара степбустов")

    for (image, draw) in hor_stripes_fill(screen, image):
        screen.send(image)
        time.sleep(0.01)
    time.sleep(4)
    for (image, draw) in vert_stripes_unfill(screen, image):
        screen.send(image)
        time.sleep(0.01)
    time.sleep(1)

    draw.text((0, 0), "и всякое разное")
    draw.text((0, 8), "   барахло")
    draw.text((0, 16), "из помойки :D")

    for (image, draw) in random_fill(screen, image):
        screen.send(image)
        time.sleep(0.01)
    time.sleep(4)
    for (image, draw) in random_unfill(screen, image):
        screen.send(image)
        time.sleep(0.01)


    for (image, _) in circles(screen, 200):
        screen.send(image)
        time.sleep(0.05)
except KeyboardInterrupt:
    screen.clear()
