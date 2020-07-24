from datetime import date

from malinalli.domain.batch import Batch


class TestBatch:
    def test_batch(self):
        batch = Batch('1', '2', 3, date(2020, 1, 1))

        assert batch.reference == '1'
        assert batch.sku == '2'
        assert batch.quantity == 3
        assert batch.eta == date(2020, 1, 1)

    def test_batch_allocate_order(self):
        assert False
