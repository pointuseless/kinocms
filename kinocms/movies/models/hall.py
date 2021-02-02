from django.db.models import Model
from django.db.models import ForeignKey, BooleanField, TextChoices, CharField
from django.db.models import CASCADE, UniqueConstraint, IntegerField
from django.utils.translation import gettext_lazy

from .cinema import Cinema
from util.fields.fields import AutoKey, NotNullableFalseBoolean


class Hall(Model):

    hall_id = AutoKey()
    cinema = ForeignKey(Cinema, on_delete=CASCADE, null=False)
    number = IntegerField()
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
    number = IntegerField()
    type = CharField(max_length=15, choices=RowType.choices, default=RowType.REGULAR)

    class Meta:
        constraints = [UniqueConstraint(fields=['hall', 'number'], name='unique_row')]


class Seat(Model):

    seat_id = AutoKey()
    row = ForeignKey(Row, on_delete=CASCADE)
    number = IntegerField()
    serviceable = BooleanField(default=True)

    class Meta:
        constraints = [UniqueConstraint(fields=['row', 'number'], name='unique_seat')]
