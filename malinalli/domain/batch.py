from typing import Optional
from datetime import date

from malinalli.domain.order import OrderLine

class Batch:
    def __init__(self,
                 reference: str,
                 sku: str,
                 quantity: int,
                 eta: Optional[date]):
        self.reference = reference
        self.sku = sku
        self.quantity = quantity
        self.eta = eta

    def allocate(self, line: OrderLine):
        self.quantity -= line.quantity
