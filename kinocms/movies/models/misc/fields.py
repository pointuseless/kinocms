from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import IntegerField, AutoField, BooleanField


class RestrictedIntegerField(IntegerField):

    def __init__(self, min_value: int = 0, max_value: int = 999, **kwargs):
        range = {'validators': [MinValueValidator(min_value), MaxValueValidator(max_value)]}
        super().__init__(self, **range, **kwargs)


class AutoKey(AutoField):

    def __init__(self):
        super().__init__(primary_key=True)


class NotNullableFalseBoolean(BooleanField):

    def __init__(self):
        super().__init__(default=False, null=False)
