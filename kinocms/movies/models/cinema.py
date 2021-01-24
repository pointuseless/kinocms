from django.db.models import Model
from django.db.models import IntegerField, CharField, ForeignKey, TextField, BooleanField
from django.db.models import CASCADE


class Cinema(Model):

    id = IntegerField(primary_key=True, verbose_name='number')
    name = CharField(max_length=63)

# TODO: use models inheritance and declare a ForeignKey custom class w/ or w/o 'primary' option
# class CinemaRelated(Model):
#
#     cinema = cinema = ForeignKey(Cinema, on_delete=CASCADE)


class CinemaDescription(Model):

    cinema = ForeignKey(Cinema, on_delete=CASCADE, primary_key=True)
    description = TextField()


class CinemaAddress(Model):

    cinema = ForeignKey(Cinema, on_delete=CASCADE, primary_key=True)
    city = CharField(max_length=31)
    street = CharField(max_length=63)
    street_number = IntegerField()


class CinemaRestriction(Model):

    cinema = ForeignKey(Cinema, on_delete=CASCADE, primary_key=True)
    restrictions = TextField(default='')

