import pytest
from cart import CartManager
from unittest import mock


@pytest.fixture(scope='session')
def cart_manager(session):
    return CartManager(session)


def skip_test_add_item(capsys, cart_manager):
    mock_user = mock.MagicMock(**{
        'id': 100,
        'name': 'mock',
        'email': 'mock@gmail.com'
    })
    mock_user.configure_mock(name='mock_user')

    mock_product = mock.MagicMock(**{
        'id': 100,
        'name': 'mock_product',
        'description': 'mock description',
        'price': 1000,
        'category_id': 'mock_category'
    })
    mock_product.configure_mock(name='mock_product')

    cart_manager.add_item(user=mock_user, product=mock_product, quantity=1)

    out, _ = capsys.readouterr()

    print(out)