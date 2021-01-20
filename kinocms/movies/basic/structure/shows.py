from __future__ import annotations

from datetime import datetime
from collections.abc import Iterator

from ..cinema_draft import Movie
from .derived import Hall, Sector
from .manipulation import PlaceAggregateIterator


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
