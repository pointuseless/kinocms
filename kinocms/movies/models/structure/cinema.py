from django.db.models import Model
from django.db.models import IntegerField, CharField, ForeignKey, TextField, BooleanField
from django.db.models import CASCADE

from kinocms.movies.models.misc.fields import AutoKey


class Cinema(Model):

    cinema_id = AutoKey()
    description = TextField(default='')
    restrictions = TextField(default='')
    city = CharField(max_length=31)
    street = CharField(max_length=63)
    street_number = IntegerField()
