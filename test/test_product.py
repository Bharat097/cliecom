import pytest
from product import ProductManager
# from unittest import mock
# from models import Product


@pytest.fixture(scope='session')
def product_manager(session):
    return ProductManager(session)


def test_add_product_negative(capsys, product_manager):
    product_manager.add_product(
        product_name='Test Product',
        desc='Test Product Description',
        price=100,
        category='Edu')

    out, _ = capsys.readouterr()

    assert 'Could not add product as Edu category not found' == out.strip('\n')


def test_list_products():
    pass


def test_view_details():
    pass
