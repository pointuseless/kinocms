from __future__ import annotations

from datetime import timedelta, datetime
from functools import singledispatchmethod
from collections.abc import Iterator


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


class Movie:

    def __init__(self, title: str, duration: timedelta):
        self.title = title
        self.duration = duration


class ContainerWithPrice:

    def __init__(self, price: int):
        self._price = price

    def get_price(self) -> int:
        return self._price

    def set_price(self, price: int) -> None:
        self._price = price


class PlaceContainerInterface:

    def clone(self) -> PlaceContainerInterface:
        raise NotImplementedError


class PlaceAggregate(PlaceContainerInterface):

    def __init__(self, nested: list[PlaceContainerInterface]):
        self._nested = nested

    def clone(self) -> PlaceContainerInterface:
        nested_clones = [nested.clone() for nested in self._nested]
        parameters = self.__dict__
        parameters['_nested'] = nested_clones
        return self.__class__(**parameters)


class PlaceAggregateWithPrice(PlaceAggregate, ContainerWithPrice)


# Возможно, место вообще не нужно. Row может хранить список мест со значение True, False
# Занят/свободен может быть Стейтом
class Place(ContainerWithPrice, PlaceContainerInterface):

    def __init__(self, identification: int, price: int = 0):
        self._occupied = False
        self._id = identification
        super().__init__(price)

    def is_occupied(self) -> bool:
        return self._occupied

    def occupy(self) -> None:
        self._occupied = True

    def free(self) -> None:
        self._occupied = False

    def clone(self) -> Place:
        return Place(self._id, self._price)


class Row(PlaceAggregate):

    def __init__(self, identification: int, places: list[Place]):
        self.id = identification
        self.places = places

    def list_places(self) -> list[Place]:
        return self.places

    def clone(self) -> Row:
        places = [place.clone() for place in self.places]
        return Row(self.id, places)

    def __iter__(self) -> Iterator[Place]:
        return iter(self.places)


class Sector:

    def __init__(self, rows: list[Row], rows_type: str):
        self.rows = rows
        self.type = rows_type

    def list_places(self) -> list[Place]:
        places = []
        [places.extend(row.list_places()) for row in self.rows]
        return places

    def clone(self) -> Sector:
        rows = [row.clone() for row in self.rows]
        return Sector(rows, self.type)

    def __iter__(self) -> Iterator[Row]:
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

    def iter_places(self) -> PlaceAggregateIterator:
        return PlaceAggregateIterator(self.sectors)

    def __iter__(self) -> Iterator[Sector]:
        return iter(self.sectors)


# TODO: Ужасный класс и нарушает все что можно!
class PriceList:

    # TODO: Потенциальные ошибки ввода (несовпадение) в Секторе и тут!
    def __init__(self, cheap: int, medium: int, vip: int):
        self._cheap = [cheap]
        self._medium = [medium]
        self._vip = [vip]
        self._prices = {'CHEAP': self._cheap,
                        'MEDIUM': self._medium,
                        'VIP': self._vip}

    @property
    def cheap(self):
        return self._cheap[0]

    @cheap.setter
    def cheap(self, price: int):
        self._cheap[0] = price

    def _get_sector_price(self, sector: Sector):
        return self._prices[sector.type][0]

    def get_place_price(self, show: Show, place: Place) -> int:
        for sector in show.hall:
            if place in sector.list_places():
                return self._get_sector_price(sector)
        else:
            raise RuntimeError('Place is not present')

    def clone(self) -> PriceList:
        return PriceList(*self._cheap, *self._medium, *self._vip)


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

    def __iter__(self) -> PlaceAggregateIterator:
        return self


class Show:

    def __init__(self, movie: Movie,
                 hall: Hall,
                 showtime: datetime,
                 price_list: PriceList):
        self.movie = movie
        self.hall = hall.clone()
        self._showtime = showtime
        self.price_list = price_list

    @property
    def showtime(self) -> datetime:
        return self._showtime

    @showtime.setter
    def showtime(self, new_showtime: datetime) -> None:
        self._showtime = new_showtime

    def get_price(self, place: Place):
        return self.price_list.get_place_price(self, place)

    def list_places(self) -> list[Place]:
        return self.hall.list_places()

    def iter_places(self) -> PlaceAggregateIterator:
        return self.hall.iter_places()

    def __iter__(self) -> Iterator[Sector]:
        return iter(self.hall)


class ShowCloneFactory:

    @staticmethod
    def from_base(base: Show,
                  new_showtime: datetime = datetime.now(),
                  link_old_price: bool = False) -> Show:
        hall_copy = base.hall.clone()
        new_price_list = base.price_list if link_old_price else base.price_list.clone()
        return Show(base.movie, hall_copy, new_showtime, new_price_list)


places = [[Place(i * 100 + j) for j in range(1, 10)] for i in range(1, 10)]
rows = [Row(i + 1, places[i]) for i in range(9)]
sectors = [Sector(rows[: 3], 'CHEAP'), Sector(rows[3: 8], 'MEDIUM'), Sector(rows[8:], 'VIP')]
hall = Hall(sectors, 'Dolby Digital')

movie = Movie('Super-Hero', timedelta(hours=1, minutes=55))

price_list = PriceList(50, 70, 90)

show = Show(movie, hall, datetime(2021, 2, 12, 14, 30), price_list)

for place in show.iter_places():
    print(place._id)

for sector in show:
    print(sector.type)

# --------- Вот теперь самое интересное: узнать цену места! --------- #

place = show.list_places()[74]
print(place._id)
print(show.get_price(place))

show2 = ShowCloneFactory.from_base(show, link_old_price=True)
print(show2.price_list.cheap)
show.price_list.cheap = 35
print(show2.price_list.cheap)
print(show2.price_list._prices)
