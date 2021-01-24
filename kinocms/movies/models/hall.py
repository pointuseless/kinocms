from django.db.models import Model
from django.db.models import ForeignKey, IntegerField, BooleanField, TextChoices, CharField
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy

from kinocms.movies.models.cinema import Cinema


class Hall(Model):

    # TODO: Composite Keys
    cinema = ForeignKey(Cinema, on_delete=CASCADE)
    hall_number = IntegerField()
    working = BooleanField(default=False)


# TODO: Row type is a separate Model
class Row(Model):

    class RowType(TextChoices):
        CHEAP = 'CHP', gettext_lazy('Cheap')
        REGULAR = 'REG', gettext_lazy('Medium')
        VIP = 'VIP', gettext_lazy('VIP')

    hall = ForeignKey(Hall, on_delete=CASCADE)
    type = CharField(max_length=15, choices=RowType.choices, default=RowType.REGULAR)


