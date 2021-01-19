from __future__ import annotations
from datetime import timedelta, datetime
from functools import singledispatchmethod
from collections.abc import Iterator


class Movie:

    def __init__(self, title: str, duration: timedelta):
        self.title = title
        self.duration = duration


# Возможно, место вообще не нужно. Row может хранить список мест со значение True, False
class Place:

    def __init__(self, identification: int):
        self.__occupied = False
        self.id = identification

    def occupy(self):
        self.__occupied = True

    def free(self):
        self.__occupied = False

    def clone(self) -> Place:
        return Place(self.id)


class Row:

    def __init__(self, identification: int, places: list[Place]):
        self.id = identification
        self.places = places

    def list_places(self):
        return self.places

    def clone(self) -> Row:
        places = [place.clone() for place in self.places]
        return Row(self.id, places)

    def __iter__(self):
        return iter(self.places)


class Sector:

    def __init__(self, rows: list[Row], row_type: str):
        self.rows = rows
        self.type = row_type

    def list_places(self) -> list[Place]:
        places = []
        [places.extend(row.list_places()) for row in self.rows]
        return places

    def clone(self) -> Sector:
        rows = [row.clone() for row in self.rows]
        return Sector(rows, self.type)

    def __iter__(self):
        return iter(self.rows)


class Hall:

    def __init__(self, sectors: list[Sector], technology: str):
        self.sectors = sectors
        self.technology = technology

    def list_places(self) -> list[Place]:
        places = []
        [places.extend(sector.list_places()) for sector in self.sectors]
        return places

    def clone(self) -> Hall:
        sectors = [sector.clone() for sector in self.sectors]
        return Hall(sectors, self.technology)

    def iter_places(self):
        return PlaceAggregateIterator(self.sectors)

    def __iter__(self):
        return iter(self.sectors)


class PriceList:

    def __init__(self, cheap: int, medium: int, vip: int):
        self.cheap = cheap
        self.medium = medium
        self.vip = vip

    def sector_price(self, sector: Sector):
        if sector.type == 'CHEAP':
            return self.cheap
        elif sector.type == 'MEDIUM':
            return self.medium
        elif sector.type == 'VIP':
            return self.vip


class PlaceAggregateIterator:

    def __init__(self, composite):
        self.nested = self.make_nested(composite)
        self.current = 0

    @singledispatchmethod
    def make_nested(self, composite) -> list[PlaceAggregateIterator]:
        return [PlaceAggregateIterator(component) for component in composite]

    @make_nested.register(Row)
    def _(self, composite) -> list[Iterator[Place]]:
        return [iter(composite)]

    def __next__(self) -> Place:
        try:
            return next(self.nested[self.current])
        except StopIteration:
            self.current += 1
            return self.__next__()
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return self


class Show:

    def __init__(self, movie: Movie,
                 hall: Hall,
                 showtime: datetime,
                 price_list: PriceList):
        self.movie = movie
        self.hall = hall.clone()
        self.showtime = showtime
        self.price_list = price_list

    def list_places(self) -> list[Place]:
        return self.hall.list_places()

    def iter_places(self) -> PlaceAggregateIterator:
        return self.hall.iter_places()

    def __iter__(self):
        return iter(self.hall)


places = [[Place(i * 100 + j) for j in range(1, 10)] for i in range(1, 10)]
rows = [Row(i + 1, places[i]) for i in range(9)]
sectors = [Sector(rows[: 3], 'CHEAP'), Sector(rows[3: 8], 'MEDIUM'), Sector(rows[8:], 'VIP')]
hall = Hall(sectors, 'Dolby Digital')

movie = Movie('Super-Hero', timedelta(hours=1, minutes=55))

price_list = PriceList(50, 70, 90)

show = Show(movie, hall, datetime(2021, 2, 12, 14, 30), price_list)

for place in show.iter_places():
    print(place.id)

for place in show.list_places():
    place.occupy()
    print(place.__dict__['_Place__occupied'])

for sector in show:
    print(sector.type)

