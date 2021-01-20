from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from functools import singledispatchmethod

from kinocms.movies.cinema_draft import Show


# Либо тикету (можно его как отображение представить), давать уже готовую для него инфу
# А создавать тикет с пережеванной инфой Фабрикой, например
# Фабрика же может заполнять билет доп инфо, например адресом кинотеатра, поздравлением с нг (новогодняя фабркиа) и тп.
class Ticket:

    def __init__(self, movie: str,
                 technology: str,
                 hall: int,
                 row: int,
                 place: int,
                 time: str,
                 price: float,
                 additional_info: str = ''):
        self.movie = movie
        self.technology = technology
        self.hall = hall
        self.row = row
        self.place = place
        self.time = time
        self.price = price
        self.additional_info = additional_info


# TODO: Не уверен, что именно так оно должно работать. Порисовать-подумать.
class Purchase:

    def __init__(self, amount: int, pay_system: PaySystemInterface):
        self.amount = amount
        self.pay_system = pay_system

    def validate(self) -> bool:
        if self.pay_system.validate_payment(self.amount):
            return True
        else:
            return False


class PaySystemInterface:
    """ Интерфейс внешней платежной системы """
    def validate_payment(self, amount: int) -> bool:
        raise NotImplementedError


# class ShowClonesRegistry:
#
#     @staticmethod
#     def from_base(base: Show,
#                   new_showtime: datetime = datetime.now(),
#                   link_old_price: bool = False) -> Show:
#         hall_copy = base.hall.clone()
#         new_price_list = base.price_list if link_old_price else base.price_list.clone()
#         return Show(base.movie, hall_copy, new_showtime, new_price_list)
#
#
# class Place:
#
#     def __repr__(self):
#         return 'place' + str(id(self))
#
#
# class PlacesContainer:
#
#     def __init__(self, contains: list[PlacesContainer]):
#         self._contains = contains
#         self.list_places: Callable[[], list[Place]] \
#             = self._detect_proper_listing_behaviour(self)
#
#     @singledispatchmethod
#     def _detect_proper_listing_behaviour(self, container: PlacesContainer) -> Callable[[], list[Place]]:
#         return lambda: list(*[content.list_places() for content in self._contains])
#
#     @_detect_proper_listing_behaviour.register(Place)
#     def _(self, content) -> Callable[[], list[Place]]:
#         return lambda: content
#
#
# class Row(PlacesContainer):
#
#     def __init__(self, rows):
#         self.rows = rows
#         super().__init__(self.rows)
#
#
# places = [Place() for _ in range(10)]
# row = Row(places)
# row2 = Row([row] * 5)
# print(row.list_places())
# print(row2.list_places())

class Hello:

    def __init__(self, ide):
        self.ide = ide


h = Hello('str')
print(h.__dict__)
