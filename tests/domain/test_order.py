from dataclasses import FrozenInstanceError

import pytest

from malinalli.domain.order import OrderLine


@pytest.fixture(scope='class')
def order_line():
    yield OrderLine('1', '231', 5)


class TestOrderLine:
    def test_order_line_properties(self, order_line):
        assert order_line.order_id == '1'
        assert order_line.sku == '231'
        assert order_line.quantity == 5

    @pytest.mark.xfail(raises=FrozenInstanceError)
    def test_order_line_is_immutable(self, order_line):
        order_line.quantity = 8
