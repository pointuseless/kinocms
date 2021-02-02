from django.db.models import Model, ForeignKey, DO_NOTHING
from django.db.models import TextField

from .map import Address
from util.fields.fields import AutoKey


class Cinema(Model):

    cinema_id = AutoKey()
    address = ForeignKey(Address, on_delete=DO_NOTHING, null=False, db_index=True)
    description = TextField(blank=True)
    restrictions = TextField(blank=True)
