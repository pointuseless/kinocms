from django.db.models import Model, CharField, DateField, TextField, DurationField

from kinocms.movies.models.misc.fields import AutoKey


class Movie(Model):

    movie_id = AutoKey()
    title = CharField(max_length=63, null=False)
    director = CharField(max_length=63, null=False)
    duration = DurationField(null=False)
    description = TextField(default='')
    genre = CharField(max_length=63)
    premier = DateField(null=False)
