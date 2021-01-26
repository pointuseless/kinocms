from __future__ import annotations
from copy import deepcopy
from datetime import timedelta

from django.db.models import ForeignKey, CASCADE, Model, UniqueConstraint, DateTimeField

from kinocms.movies.models.structure.hall import Hall
from kinocms.util.fields.fields import RestrictedIntegerField, AutoKey
from kinocms.movies.models.schedules.movie import Movie
from kinocms.util.fields.func import setup_fields_params

DEFAULT_RESERVATION_STOP = timedelta(minutes=30)    # TODO: how? Maybe via separate service that deletes expired...


class Show(Model):

    show_id = AutoKey()
    datetime = DateTimeField()
    hall = ForeignKey(Hall, on_delete=CASCADE)
    movie = ForeignKey(Movie, on_delete=CASCADE)
    vip_price = RestrictedIntegerField()
    medium_price = RestrictedIntegerField()
    cheap_price = RestrictedIntegerField()

    setup_fields_params([datetime, hall, movie, vip_price, medium_price, cheap_price],
                        {'null': False, 'db_index': True})

    class Meta:
        constraints = [UniqueConstraint(fields=['datetime', 'hall'], name='unique_show')]

    def replicate(self,
                  datetime: datetime = None,
                  hall: Hall = None,
                  vip_price: int = None,
                  medium_price: int = None,
                  cheap_price: int = None) -> Show:

        params = {'datetime': datetime,
                  'hall': hall,
                  'vip_price': vip_price,
                  'medium_price': medium_price,
                  'cheap_price': cheap_price}

        clone = deepcopy(self)
        clone.show_id = None
        clone.pk = None
        clone.__dict__ |= {key: value for key, value in params if value is not None}

        return clone
