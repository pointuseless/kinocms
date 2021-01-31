from django.db.models import Model, UniqueConstraint, CharField, ForeignKey, DO_NOTHING

from kinocms.util.fields.fields import AutoKey
from kinocms.util.fields.func import setup_fields_params


class City(Model):

    city_id = AutoKey()
    region = CharField()
    city = CharField()

    setup_fields_params([region, city],
                        {'max_length': 31, 'null': False, 'db_index': True})

    class Meta:
        constraints = [UniqueConstraint(fields=['region', 'city'], name='unique_city')]


class Address(Model):

    address_id = AutoKey()
    city = ForeignKey(City, on_delete=DO_NOTHING, null=False, db_index=True)
    street = CharField()
    building = CharField()

    setup_fields_params([street, building],
                        {'max_length': 31, 'null': False})

    class Meta:
        constraints = [UniqueConstraint(fields=['city', 'street', 'building'], name='unique_address')]
