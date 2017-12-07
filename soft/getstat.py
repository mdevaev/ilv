#!/usr/bin/env python3


import sys
import re
import math

import requests

from ilv import Screen
from ilv import Font
from ilv import make_image


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
screen = Screen(sys.argv[1] if len(sys.argv) >= 2 else None)
(image, draw) = make_image()
draw.text((0, 0), " ВК    АК    ТП ")
draw.text((0, 8), "%(vk_subs)5s %(acomics_subs)4s %(tapastic_subs)5s" % {
    **get_vk_stat(),
    **get_acomics_stat(),
    **get_tapastic_stat(),
})
draw.text((0, 16), "ПТ: %(patreon_subs)s / %(patreon_pledge)s" % get_patreon_stat())
#draw.text((0, 0), "vk:%(vk_subs)s A:%(acomics_subs)s" % {**get_vk_stat(), **get_acomics_stat()})
#draw.text((0, 0), "Вконтач: %(vk_subs)7s" % get_vk_stat())
#draw.text((0, 8), "Тапастик: %(tapastic_subs)6s" % get_tapastic_stat())
#draw.text((0, 16), "Акомикс: %(acomics_subs)7s" % get_acomics_stat())
#draw.text((0, 16), "Патреон: %(patreon_pledge)7s" % get_patreon_stat())
# screen.print(image)
screen.set_enabled(True)
screen.send(image)
