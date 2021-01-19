from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from functools import singledispatchmethod

from kinocms.movies.cinema_draft import Show


class ShowClonesRegistry:

    @staticmethod
    def from_base(base: Show,
                  new_showtime: datetime = datetime.now(),
                  link_old_price: bool = False) -> Show:
        hall_copy = base.hall.clone()
        new_price_list = base.price_list if link_old_price else base.price_list.clone()
        return Show(base.movie, hall_copy, new_showtime, new_price_list)


class Place:

    def __repr__(self):
        return 'place' + str(id(self))


class PlacesContainer:

    def __init__(self, contains: list[PlacesContainer]):
        self._contains = contains
        self.list_places: Callable[[], list[Place]] \
            = self._detect_proper_listing_behaviour(self)

    @singledispatchmethod
    def _detect_proper_listing_behaviour(self, container: PlacesContainer) -> Callable[[], list[Place]]:
        return lambda: list(*[content.list_places() for content in self._contains])

    @_detect_proper_listing_behaviour.register(Place)
    def _(self, content) -> Callable[[], list[Place]]:
        return lambda: content


class Row(PlacesContainer):

    def __init__(self, rows):
        self.rows = rows
        super().__init__(self.rows)


places = [Place() for _ in range(10)]
row = Row(places)
row2 = Row([row] * 5)
print(row.list_places())
print(row2.list_places())
