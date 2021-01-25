from __future__ import annotations

from datetime import timedelta

from django.db.models import ForeignKey, CASCADE, Model, UniqueConstraint, DateTimeField

from kinocms.movies.models.structure.hall import Hall
from kinocms.movies.models.misc.fields import RestrictedIntegerField, AutoKey
from kinocms.movies.models.schedules.movie import Movie


DEFAULT_RESERVATION_STOP = timedelta(minutes=30)


class Show(Model):

    show_id = AutoKey()
    datetime = DateTimeField(null=False)
    hall = ForeignKey(Hall, on_delete=CASCADE, null=False)
    movie = ForeignKey(Movie, on_delete=CASCADE, null=False)
    vip_price = RestrictedIntegerField(null=False)
    medium_price = RestrictedIntegerField(null=False)
    cheap_price = RestrictedIntegerField(null=False)
    stop_reservation = DateTimeField(default=timedelta())    # TODO: auto-calculate howto? BUT w/o func dependency!

    class Meta:
        constraints = [UniqueConstraint(fields=['datetime', 'hall'], name='unique_show')]

    def replicate(self, **kwargs) -> Show:
        pass
