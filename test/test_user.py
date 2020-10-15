import pytest
from user import UserManager
from unittest import mock
from models import User


@pytest.fixture(scope='session')
def user_manager(session):
    return UserManager(session)


def test_add_user(user_manager):
    user_manager.add_user('user_name', 'user@gmail.com', '1234')

    res = user_manager.session.query(User).filter_by(email='user@gmail.com').one()

    assert res.name == 'user_name'


def test_list_user(user_manager):
    users = user_manager.list_users()

    assert len(users) == 1


def test_list_bills(user_manager):
    item1 = mock.Mock(
        **{
            'id': 10,
            'product.name': 'Car',
            'quantity': 1
        })
    item2 = mock.Mock(
        **{
            'id': 20,
            'product.name': 'Mobile',
            'quantity': 2
        })
    items_mock = [item1, item2]

    orders_mock = [mock.Mock(
        **{
            'id': 1,
            'order_amount': 5000,
            'created': '10/10/2020',
            'order_items': items_mock
        })]

    user = mock.Mock(**{'orders': orders_mock})

    bills = user_manager.list_bills(user)

    assert len(bills) == len(orders_mock)
    assert len(bills[1]) == 3
    assert bills[1]['items']['Mobile'] == 2 and bills[1]['items']['Car'] == 1
