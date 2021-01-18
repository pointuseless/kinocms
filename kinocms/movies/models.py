from __future__ import annotations
from datetime import datetime, timedelta

from django.db import models


class Movie(models.Model):















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



