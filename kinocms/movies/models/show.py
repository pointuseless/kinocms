from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import TimeField, ForeignKey, CASCADE, Model, IntegerField, DateField

from kinocms.movies.models.hall import Hall
from kinocms.movies.models.movie import Movie


# TODO: Not Nullable Fields are starting to be a pain in the ass. I should better make Not Nullable Field.
class Show(Model):

    date = DateField(null=False)
    time = TimeField(null=False)
    hall = ForeignKey(Hall, on_delete=CASCADE, null=False)
    movie = ForeignKey(Movie, on_delete=CASCADE, null=False)


# TODO: 'clean' sth --- Google it...
# TODO: This maybe belongs to show as well. It's pretty unique info.
class ShowPrice(Model):

    class ShowPriceField(IntegerField):

        def __init__(self, min_value=0, max_value=999, **kwargs):
            range = {'validators': [MinValueValidator(min_value), MaxValueValidator(max_value)]}
            super().__init__(self, null=False, **range, **kwargs)

    show = ForeignKey(Show, on_delete=CASCADE, null=False, primary_key=True)
    vip = ShowPriceField()
    medium = ShowPriceField()
    cheap = ShowPriceField()
