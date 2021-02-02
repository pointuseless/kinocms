from django.db.models import Model, CharField, DateField, TextField, DurationField, ImageField

from util.fields.fields import AutoKey
from util.fields.func import setup_fields_params


# TODO: technologies
class Movie(Model):

    movie_id = AutoKey()
    title = CharField(db_index=True)
    director = CharField(blank=True)
    duration = DurationField(null=False)
    description = TextField(blank=True)
    genre = CharField(blank=True)
    premier = DateField(null=False, db_index=True)
    picture = ImageField(upload_to='movies')

    setup_fields_params([title, director, genre], dict(null=False, max_length=63))
