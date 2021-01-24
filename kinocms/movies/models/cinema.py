from django.db.models import Model
from django.db.models import IntegerField, CharField, ForeignKey, TextField, BooleanField
from django.db.models import CASCADE


class Cinema(Model):

    name = CharField(max_length=63)
    description = TextField(default='')
    restrictions = TextField(default='')


class CinemaAddress(Model):

    cinema = ForeignKey(Cinema, on_delete=CASCADE, primary_key=True)
    city = CharField(max_length=31)
    street = CharField(max_length=63)
    street_number = IntegerField()
