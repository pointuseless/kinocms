from django.db.models import Model, CharField, ForeignKey, CASCADE, DateField, TimeField, TextField


class Movie(Model):

    title = CharField(max_length=63, null=False)
    director = CharField(max_length=63, null=False)
    duration = TimeField(null=False)
    description = TextField(default='')
    genre = CharField(max_length=63)


# TODO: merge with Movie, it's pretty much unique.
class Premier(Model):

    movie = ForeignKey(Movie, on_delete=CASCADE, null=False, primary_key=True)
    date = DateField(null=False)
