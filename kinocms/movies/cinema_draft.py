from __future__ import annotations

from datetime import timedelta, datetime
from functools import singledispatchmethod
from collections.abc import Iterator
from typing import Union


class Movie:

    def __init__(self, title: str, duration: timedelta):
        self.title = title
        self.duration = duration


class PlaceContainerInterface:

    def clone(self) -> PlaceContainerInterface:
        raise NotImplementedError


class PriceContainer(PlaceContainerInterface):

    def __init__(self, price: int = 0, **kwargs):
        self._price = price
        super().__init__(**kwargs)

    def get_price(self) -> int:
        return self._price

    def set_price(self, price: int) -> None:
        self._price = price

    def clone(self) -> PriceContainer:
        raise NotImplementedError


class PlaceAggregate(PlaceContainerInterface):

    def __init__(self, nested: list[PriceContainer], **kwargs):
        self._nested = nested
        super().__init__(**kwargs)

    @property
    def places(self) -> list[Place]:
        return list(self.iter_places())

    @property
    def nested(self) -> list[PriceContainer]:
        return self._nested

    def clone(self) -> PlaceAggregate:
        nested_clones = [nested.clone() for nested in self._nested]
        parameters = self.__dict__
        parameters['_nested'] = nested_clones
        clone = object.__new__(self.__class__)
        clone.__dict__ = parameters
        return clone

    def iter_places(self) -> PlaceAggregateIterator:
        return PlaceAggregateIterator(self)

    def __iter__(self) -> Iterator[Union[PriceContainer, PlaceAggregate]]:
        return iter(self.nested)


# Возможно, место вообще не нужно. Row может хранить список мест со значение True, False
# Занят/свободен может быть Стейтом
class Place(PriceContainer):

    def __init__(self, identification: int, price: int = 0):
        self._occupied = False
        self._id = identification
        super().__init__(price=price)

    def is_occupied(self) -> bool:
        return self._occupied

    def occupy(self) -> None:
        self._occupied = True

    def free(self) -> None:
        self._occupied = False

    def clone(self) -> Place:
        return Place(self._id, self.get_price())


class Row(PlaceAggregate, PriceContainer):

    def __init__(self, identification: int, places: list[Place], price: int = 0):
        self.id = identification
        super().__init__(nested=places, price=price)

    def set_price(self, price: int) -> None:
        super().set_price(price)
        for each in self.nested:
            each.set_price(price)


class Sector(PlaceAggregate, PriceContainer):

    def __init__(self, rows: list[Row], rows_type: str, price: int = 0):
        self.type = rows_type
        super().__init__(nested=rows, price=price)

    @property
    def rows(self) -> list[Row]:
        return list(iter(self))

    def set_price(self, price: int) -> None:
        super().set_price(price)
        for each in self.nested:
            each.set_price(price)


class Hall(PlaceAggregate):

    def __init__(self, sectors: list[Sector], technology: str):
        self.technology = technology
        super().__init__(nested=sectors)

    @property
    def sectors(self) -> list[Sector]:
        return list(iter(self))


class PlaceAggregateIterator:

    def __init__(self, composite: PlaceAggregate):
        self.nested = self.make_nested(composite)
        self.current = 0

    @singledispatchmethod
    def make_nested(self, composite: PlaceAggregate) -> list[PlaceAggregateIterator]:
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

    def __iter__(self) -> PlaceAggregateIterator:
        return self


class Show:

    def __init__(self, movie: Movie,
                 hall: Hall,
                 showtime: datetime):
        self.movie = movie
        self.hall = hall.clone()
        self._showtime = showtime

    @property
    def showtime(self) -> datetime:
        return self._showtime

    @showtime.setter
    def showtime(self, new_showtime: datetime) -> None:
        self._showtime = new_showtime

    def iter_places(self) -> PlaceAggregateIterator:
        return self.hall.iter_places()

    def __iter__(self) -> Iterator[Sector]:
        return iter(self.hall)


places = [[Place(i * 100 + j) for j in range(1, 10)] for i in range(1, 10)]
rows = [Row(i + 1, places[i]) for i in range(9)]
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
