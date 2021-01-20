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
