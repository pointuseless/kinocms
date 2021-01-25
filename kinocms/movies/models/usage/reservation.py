from datetime import timedelta

from django.db.models import Model, ForeignKey, DO_NOTHING, UniqueConstraint, DateTimeField
from django.utils import timezone

from kinocms.movies.models.misc.fields import AutoKey
from kinocms.movies.models.schedules.show import Show
from kinocms.movies.models.structure.hall import Seat


DEFAULT_TIMEOUT = timezone.now() + timedelta(minutes=30)


class Reservation(Model):

    reservation_id = AutoKey()
    show = ForeignKey(Show, on_delete=DO_NOTHING, null=False)
    seat = ForeignKey(Seat, on_delete=DO_NOTHING, null=False)
    expires = DateTimeField(default=DEFAULT_TIMEOUT)

    class Meta:
        constraints = [UniqueConstraint(fields=['show', 'seat_number'], name='unique_reservation')]
