from django.db.models import Model, ForeignKey, DO_NOTHING

from kinocms.movies.models.misc.fields import AutoKey
from kinocms.movies.models.schedules.show import Show


class Ticket(Model):

    ticket_id = AutoKey()
    show = ForeignKey(Show, on_delete=DO_NOTHING, null=False)