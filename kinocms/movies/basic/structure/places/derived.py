from __future__ import annotations

from functools import singledispatchmethod
from typing import Union
from collections.abc import Iterator

from kinocms.movies.basic.structure.places.abc import PriceContainer, \
    CloneablePlaceAggregate


class PlaceAggregate(CloneablePlaceAggregate):

    @property
    def places(self) -> list[Place]:
        return list(self.iter_places())

    def iter_places(self) -> PlaceAggregateIterator:
        return PlaceAggregateIterator(self)

    def __iter__(self) -> Iterator[Union[PriceContainer, PlaceAggregate]]:
        return iter(self._nested)


class Place(PriceContainer):

    def __init__(self, identification: int, price: int = 0):
        self._occupied = False
        self._id = identification
        super().__init__(price=price)

    @property
    def id(self) -> int:
        return self._id

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


class Constructor:

    @classmethod
    def create_places(cls, quantity: int, row_index: int) -> list[Place]:
        return [Place(row_index * 1000 + i) for i in range(1, quantity + 1)]

    @classmethod
    def create_rows(cls, first: int, last: int, places: int) -> list[Row]:
        rows = []
        for i in range(first, last + 1):
            row = Row(i, cls.create_places(places, i))
            rows.append(row)
        return rows

    @classmethod
    def create_row(cls, identification: int, places: int) -> Row:
        return Row(identification, cls.create_places(places, identification))


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
