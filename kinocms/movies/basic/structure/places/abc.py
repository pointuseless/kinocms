from __future__ import annotations


class CloneablePlaceContainerInterface:

    def clone(self) -> CloneablePlaceContainerInterface:
        raise NotImplementedError


class PriceContainer(CloneablePlaceContainerInterface):

    def __init__(self, price: int = 0, **kwargs):
        self._price = price
        super().__init__(**kwargs)

    def get_price(self) -> int:
        return self._price

    def set_price(self, price: int) -> None:
        self._price = price

    def clone(self) -> PriceContainer:
        raise NotImplementedError


class CloneablePlaceAggregate(CloneablePlaceContainerInterface):

    def __init__(self, nested: list[PriceContainer], **kwargs):
        self._nested = nested
        super().__init__(**kwargs)

    @property
    def nested(self) -> list[PriceContainer]:
        return self._nested

    def clone(self) -> CloneablePlaceAggregate:
        nested_clones = [nested.clone() for nested in self._nested]
        parameters = self.__dict__
        parameters['_nested'] = nested_clones
        clone = object.__new__(self.__class__)
        clone.__dict__ = parameters
        return clone
