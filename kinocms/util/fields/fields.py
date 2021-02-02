from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import IntegerField, AutoField, BooleanField


# class RestrictedIntegerField(IntegerField):
#     """Integer Field with given range of values only accepted"""
#     def __init__(self, *args, min_value=1, max_value=999, **kwargs):
#         self.validators_ = [MinValueValidator(min_value), MaxValueValidator(max_value)]
#         super().__init__(self, *args, **kwargs)
#
#     def deconstruct(self):
#         name, path, args, kwargs = super().deconstruct()
#         if self.validators_
#         return name, path, args, kwargs


class AutoKey(AutoField):
    """Auto Integer Primary Key"""
    def __init__(self, *args, **kwargs):
        kwargs['primary_key'] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['primary_key']
        return name, path, args, kwargs


class NotNullableFalseBoolean(BooleanField):
    """Not Null Boolean Field with default value False"""
    def __init__(self, *args, **kwargs):
        kwargs['default'] = False
        kwargs['null'] = False
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['default']
        return name, path, args, kwargs
