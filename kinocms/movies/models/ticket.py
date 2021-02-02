from django.db.models import Model, ForeignKey, DO_NOTHING

from util.fields.fields import AutoKey
from .show import Show


class Ticket(Model):

    ticket_id = AutoKey()
    show = ForeignKey(Show, on_delete=DO_NOTHING, null=False)
