from django.db.models import Model, ForeignKey, CASCADE, DO_NOTHING
from django.db.models import TextField, UniqueConstraint

from kinocms.movies.models.map.map import Address
from kinocms.util.fields.fields import AutoKey


class Cinema(Model):

    cinema_id = AutoKey()
    address = ForeignKey(Address, on_delete=DO_NOTHING, null=False, db_index=True)
    description = TextField(default='')
    restrictions = TextField(default='')
