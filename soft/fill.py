#!/usr/bin/env python3

from pixtube.screens.ilv import Screen

screen = Screen("/dev/ttyACM0")
screen.set_enabled()
(image, draw) = screen.make_image()
draw.rectangle((0, 0, 94, 22), fill=255)
screen.send(image)
