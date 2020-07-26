from datetime import date

import pytest

from malinalli.domain import Batch, OrderLine


@pytest.fixture
def batch():
    yield Batch('batch-1', 'sku-1', 5, date(2020, 1, 1))


class TestBatch:
    def test_batch(self, batch):
        assert batch.reference == 'batch-1'
        assert batch.sku == 'sku-1'
        assert batch.available_quantity == 5
        assert batch.eta == date(2020, 1, 1)

    def test_batch_allocate_order(self, batch):
        batch.allocate(OrderLine('order_line-1', 'sku-1', 2))
        assert batch.allocated_quantity == 2
        assert batch.available_quantity == 3

        batch.allocate(OrderLine('order_line-1', 'sku-1', 3))
        assert batch.allocated_quantity == 5
        assert batch.available_quantity == 0

    def test_batch_deallocated_order(self, batch):
        order_line = OrderLine('order_line-1', 'sku-1', 2)

        assert batch.available_quantity == 5

        batch.allocate(order_line)
        assert batch.available_quantity == 3

        batch.deallocate(order_line)
        assert batch.available_quantity == 5

    def test_batch_allocated_quantity(self, batch):
        order_line = OrderLine('order_line-1', 'sku-1', 2)

        assert batch.allocated_quantity == 0

        batch.allocate(order_line)
        assert batch.allocated_quantity == 2

        batch.allocate(OrderLine('order_line-1', 'sku-1', 3))
        assert batch.allocated_quantity == 5

    def test_batch_available_quantity(self, batch):
        order_line = OrderLine('order_line-1', 'sku-1', 2)

        assert batch.available_quantity == 5

        batch.allocate(order_line)
        assert batch.available_quantity == 3

        batch.allocate(OrderLine('order_line-1', 'sku-1', 3))
        assert batch.available_quantity == 0

    def test_batch_can_allocate(self, batch):
        order_line = OrderLine('order_line-1', 'sku-1', 5)

        assert batch.can_allocate(order_line)

    def test_batch_can_not_allocate_with_different_sku(self, batch):
        order_line = OrderLine('order_line-1', 'sku-2', 4)

        assert not batch.can_allocate(order_line)

    def test_batch_can_not_allocate_with_batch_quantity_smaller_than_required(self, batch):
        order_line = OrderLine('order_line-1', 'sku-1', 6)

        assert not batch.can_allocate(order_line)

    def test_batch_can_deallocate(self, batch):
        order_line = OrderLine('order_line-1', 'sku-1', 4)

        assert not batch.can_deallocate(order_line)

        batch.allocate(order_line)
        assert batch.can_deallocate(order_line)

    def test_batch_equals(self, batch):
        batch2 = Batch('batch-1', 'sku-2', 10, date(2020, 2, 2))

        assert batch == batch2

    def test_batch_not_equals(self, batch):
        batch2 = Batch('batch-2', 'sku-1', 5, date(2020, 1, 1))

        assert batch != batch2

    def test_batch_hash(self, batch):
        assert hash(batch) == hash(batch.reference)

    def test_batch_str(self, batch):
        assert str(batch) == ('Batch(reference=batch-1, sku=sku-1, '
                              'available_quantity=5, eta=2020-01-01)')
