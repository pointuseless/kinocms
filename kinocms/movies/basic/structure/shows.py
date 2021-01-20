from __future__ import annotations

from datetime import datetime
from collections.abc import Iterator


from kinocms.movies.basic.structure.places.derived import Hall, PlaceAggregateIterator, Sector
from kinocms.movies.basic.structure.movies import Movie


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

    # TODO: линковка прайс-листов с возможностью отцепить
    @staticmethod
    def from_base(base: Show,
                  new_showtime: datetime = datetime.now(),
                  link_old_price: bool = False) -> Show:
        hall_copy = base.hall.clone()
        return Show(base.movie, hall_copy, new_showtime)
