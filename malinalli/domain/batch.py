from typing import Optional
from datetime import date

from malinalli.domain.order import OrderLine


class Batch:
    def __init__(self,
                 reference: str,
                 sku: str,
                 quantity: int,
                 eta: Optional[date]) -> None:
        self.reference = reference
        self.sku = sku
        self.eta = eta
        self._quantity = quantity
        self._allocations = set()

    def allocate(self, order_line: OrderLine) -> None:
        if self.can_allocate(order_line):
            self._allocations.add(order_line)

    def deallocate(self, order_line: OrderLine) -> None:
        if self.can_deallocate(order_line):
            self._allocations.remove(order_line)

    @property
    def allocated_quantity(self) -> int:
        return sum(order_line.quantity
                   for order_line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._quantity - self.allocated_quantity

    def can_allocate(self, order_line: OrderLine) -> bool:
        return (self.sku == order_line.sku and
                self.available_quantity >= order_line.quantity)

    def can_deallocate(self, order_line: OrderLine) -> bool:
        return order_line in self._allocations

    def __eq__(self, other) -> bool:
        if not isinstance(other, Batch):
            return False

        return other.reference == self.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __str__(self) -> str:
        return (f'Batch(reference={self.reference}, sku={self.sku}, '
                f'available_quantity={self._quantity}, eta={self.eta})')
