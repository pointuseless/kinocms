from django.db.models import Model
from django.db.models import ForeignKey, IntegerField, BooleanField, TextChoices, CharField
from django.db.models import CASCADE, UniqueConstraint
from django.utils.translation import gettext_lazy

from kinocms.movies.models.structure.cinema import Cinema
from kinocms.movies.models.misc.fields import RestrictedIntegerField, AutoKey, NotNullableFalseBoolean


class Hall(Model):

    hall_id = AutoKey()
    cinema = ForeignKey(Cinema, on_delete=CASCADE, null=False)
    number = RestrictedIntegerField(min_value=1, max_value=19)
    working = NotNullableFalseBoolean()
    two_dim = NotNullableFalseBoolean()
    three_dim = NotNullableFalseBoolean()
    imax = NotNullableFalseBoolean()

    class Meta:
        constraints = [UniqueConstraint(fields=['cinema', 'number'], name='unique_hall')]


class Row(Model):

    class RowType(TextChoices):
        CHEAP = 'CHP', gettext_lazy('Cheap')
        REGULAR = 'REG', gettext_lazy('Medium')
        VIP = 'VIP', gettext_lazy('VIP')

    row_id = AutoKey()
    hall = ForeignKey(Hall, on_delete=CASCADE)
    number = RestrictedIntegerField(min_value=1, max_value=19)
    type = CharField(max_length=15, choices=RowType.choices, default=RowType.REGULAR)

    class Meta:
        constraints = [UniqueConstraint(fields=['hall', 'number'], name='unique_row')]


class Seat(Model):

    seat_id = AutoKey()
    row = ForeignKey(Row, on_delete=CASCADE)
    number = RestrictedIntegerField(min_value=1, max_value=99)
    serviceable = BooleanField(default=True)

    class Meta:
        constraints = [UniqueConstraint(fields=['row', 'number'], name='unique_seat')]
