import importlib.util
import re
from typing import Any, Type


from django.db.models import Field


def setup_fields_params(fields: list[Field], params: dict[str, Any]) -> None:
    """Sets given key-value parameters for every field in a list"""
    for field in fields:
        for param_key, param_value in params.items():
            field.__dict__[param_key] = param_value


def _setup_fields_in_source(cls: Type, params: dict[str, str]) -> None:
    """Prints given parameters into model's fields declarations right in it's source code"""
    module = importlib.import_module(cls.__module__)
    with open(module.__file__, 'w+') as src:
        code = src.read()
