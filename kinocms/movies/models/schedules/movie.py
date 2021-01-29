from django.db.models import Model, CharField, DateField, TextField, DurationField

from kinocms.util.fields.fields import AutoKey
from kinocms.util.fields.func import setup_fields_params


# TODO: technologies
class Movie(Model):

    movie_id = AutoKey()
    title = CharField(db_index=True)
    director = CharField()
    duration = DurationField(null=False)
    description = TextField(default='')
    genre = CharField()
    premier = DateField(null=False, db_index=True)

    setup_fields_params([title, director, genre], dict(null=False, max_length=63))
