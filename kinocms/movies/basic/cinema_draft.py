from __future__ import annotations

from datetime import timedelta, datetime
from functools import singledispatchmethod
from collections.abc import Iterator
from typing import Union

from kinocms.movies.basic.structure.derived import Constructor, Sector, Hall
from kinocms.movies.basic.structure.shows import Show


class Movie:

    def __init__(self, title: str, duration: timedelta):
        self.title = title
        self.duration = duration


# --------- Начало демонстрации --------- #

rows = Constructor.create_rows(1, 9, 15)
sectors = [Sector(rows[: 3], 'CHEAP'), Sector(rows[3: 8], 'MEDIUM'), Sector(rows[8:], 'VIP')]
hall = Hall(sectors, 'Dolby Digital')

movie = Movie('Super-Hero', timedelta(hours=1, minutes=55))

show = Show(movie, hall, datetime(2021, 2, 12, 14, 30))

for place in show.iter_places():
    print(place._id)

for sector in show:
    print(sector.type)

# --------- Вот теперь самое интересное: узнать цену места! --------- #

show.hall.sectors[0].set_price(45)
place = show.hall.sectors[0].rows[0].places[3]
print(place.get_price())
