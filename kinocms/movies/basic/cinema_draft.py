from __future__ import annotations

from datetime import timedelta, datetime

from kinocms.movies.basic.structure.places.derived import Constructor, Sector, Hall
from kinocms.movies.basic.structure.movies import Movie
from kinocms.movies.basic.structure.shows import Show


# --------- Начало демонстрации --------- #

if __name__ == '__main__':

    rows = Constructor.create_rows(1, 9, 15)
    sectors = [Sector(rows[: 3], 'CHEAP'), Sector(rows[3: 8], 'MEDIUM'), Sector(rows[8:], 'VIP')]
    hall = Hall(sectors, 'Dolby Digital')

    movie = Movie('Super-Hero', timedelta(hours=1, minutes=55))

    show = Show(movie, hall, datetime(2021, 2, 12, 14, 30))

    for place in show.iter_places():
        print(place.id)

    for sector in show:
        print(sector.type)

# --------- Вот теперь самое интересное: узнать цену места! --------- #

    show.hall.sectors[0].set_price(45)
    place = show.hall.sectors[0].rows[0].places[3]
    print(place.get_price())

# --------- Создать показ на базе предыдущего --------- #

    show2 = Show.from_base(show)
    show2.hall.sectors[0].set_price(50)
    place = show.hall.sectors[0].rows[0].places[3]
    print(place.get_price())
