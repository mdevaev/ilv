#!/usr/bin/env python3


import sys
import re
import math

import requests

from ilv import Screen
from ilv import Font


def http_get(url):
    response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return response


def get_acomics_stat():
    response = http_get("http://acomics.ru/~sammy/about")
    return {
        "acomics_subs": re.search(r"<p><b>Количество подписчиков:</b>\s*(\d+)</p>", response.text).group(1),
    }


def get_tapastic_stat():
    response = http_get("https://tapastic.com/series/Sammy")
    return {
        "tapastic_subs": re.search(r"subscribersCount : (\d+)", response.text).group(1),
    }


def get_patreon_stat():
    response = http_get("https://patreon.com/rtstudio")
    return {
        "patreon_subs": re.search(r"\"patron_count\": (\d+)", response.text).group(1),
        "patreon_pledge": "$" + str(math.ceil(int(re.search(r"\"pledge_sum\": (\d+)", response.text).group(1)) / 100)),
    }


def get_vk_stat():
    response = http_get("https://vk.com/randomtanstudio")
    return {
        "vk_subs": "".join(re.search(r"Подписчики <em class=\"pm_counter\">(\d+)<span class=\"num_delim\">"
                                     r" </span>(\d+)</em>", response.text).groups()),
    }


# https://fontstruct.com/gallery/tag/386/5x7
font = Font([
    "ilv/data/fonts/Lcd-2.ttf",
    "!ilv/data/fonts/Lcd-2.extra.yaml",
])

screen = Screen(sys.argv[1] if len(sys.argv) >= 2 else None)
screen.draw_text(0, 0, font, """
Вконтач: %(vk_subs)7s
Тапастик: %(tapastic_subs)6s
Патреон: %(patreon_pledge)7s
""".strip() % {
    **get_vk_stat(),
    **get_tapastic_stat(),
    **get_patreon_stat(),
})

#screen.draw_text(0, 0, font, "Акомикс: %7d" % get_acomics_subs())
#screen.draw_text(0, 8, font, "Тапастик: %6d" % get_tapastic_subs())
#print(get_acomics_stat())
#print(get_tapastic_stat())
screen.print()
screen.send()
