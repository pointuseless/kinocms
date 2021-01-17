from __future__ import annotations
from datetime import datetime, timedelta

from django.db import models


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


class Theater:

    def __init__(self, name: str,
                 address: str,
                 halls: list[Hall]):
        self.name = name
        self.address = address
        self.halls = halls


# Использование этого класса под вопросом
class Technology:

    def __init__(self, name: str, basic_price: int):
        self.name = name
        self.basic_price = basic_price


# TODO: типы залов 3D, 2D, etc, с возможностью легко добавить новую технологию
# Возможно, Медиатором ходить по всем участникам сеанса и считать цену... Только если автоматически!
# Использование поддержки технологий под вопросом
# TODO: наверное, сделать композит и клонировать в объект сеанса...
class Hall:

    def __init__(self, technology: Technology,
                 rows: list[Row],
                 works: bool = False):
        self.technology = technology
        self.rows = rows
        self.works = works

    def clone(self) -> Hall:
        pass


class ShowFactory:

    @staticmethod
    def create_show(movie: Movie, hall: Hall, when: datetime) -> Show:
        if hall.technology not in movie.supported_technologies:
            raise RuntimeError('This movie cannot be shown using this technology. Please choose appropriate hall')
        else:
            return Show(movie, hall.clone(), when)


# Использование price ratio под вопросом - цены могут устанавливаться полностью вручную
# Использование visible под вопросом - может не понадобиться
# TODO: Кто-то должен проверять, что фильм будет показан в зале с нужной технологией и наоборот
# TODO: Кто-то должен проверять, что сеанс будет создан не раньше премьеры
# TODO: Кто-то должен проверять, что сеанс будет создан не в прошлом
# TODO: Кто-то должен проверять, что сеанс будет создан в рамках расписания
class Show:

    def __init__(self, movie: Movie,
                 hall: Hall,
                 when: datetime,
                 price_ratio: float = 1.0,
                 visible: bool = True):
        self.movie = movie
        self.hall = hall
        self.when = when


class Row:

    def __init__(self, places: list[Place]):
        self.places = places


# Наличие отдельного класса под вопросом
class TemporalReservation:

    def __init__(self, place: Place, timer: timedelta):
        self.place = place
        self.timer = timer


class Place:

    def __init__(self):
        self.free = True

    def occupy(self) -> None:
        self.free = False


# Использование поддержки технологий под вопросом
class Movie:

    def __init__(self, title: str,
                 duration: timedelta,
                 supported_technologies: list[Technology],
                 description: str = ''):
        self.title = title
        self.duration = duration
        self.supported_technologies = supported_technologies
        self.description = description
