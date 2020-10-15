import pytest
from category import CategoryManager


@pytest.fixture(scope='session')
def category_manager(session):
    return CategoryManager(session)


def test_add_category(capsys, category_manager):
    category_manager.add_category(category_name='Automobile')

    out, _ = capsys.readouterr()

    assert 'category Automobile added successfully' == out.strip('\n')


def test_list_categories(category_manager):
    categories = category_manager.list_categories()

    assert len(categories) == 1
    assert categories[0].name == 'Automobile'


def test_list_products_by_category(category_manager):
    products = category_manager.list_products_by_category('Automobile')

    assert products == []
