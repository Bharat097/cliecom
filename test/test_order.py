import pytest
from order import OrderManager
from unittest import mock


@pytest.fixture(scope='session')
def order_manager(session):
    return OrderManager(session)


def test_is_discount(order_manager):
    order_manager.order = mock.Mock(**{'order_amount': 11000})
    total, status = order_manager.is_discount()

    assert total == 11000, status is True
