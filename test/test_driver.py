import driver
import pytest


@pytest.fixture(scope='session')
def driver_manager(session):
    return driver.Driver(session)


output = []
input_values = []


def mock_input(s=''):
    global output, input_values

    output.append(s)
    print(*output)
    output.clear()
    user_input = input_values.pop(0)
    print(user_input)
    return user_input


def test_create_user(driver_manager):
    global input_values, output

    input_values += [
        'Bharat', 'bharat@gmail.com', '1234',
    ]
    output = []

    driver.input = mock_input
    driver_manager.create_user()

    assert True


def test_login(driver_manager):
    global input_values, output

    input_values += [
        'bharat@gmail.com', '1234',
    ]
    output = []

    driver.input = mock_input
    driver.print = lambda s: output.append(s)

    driver_manager.login()

    assert 'Bharat logged in successfully' == output[0]


def test_start_admin_flow_1_2(driver_manager):
    global input_values, output

    input_values += [
        '1',
        'Education',
        '',
        '2',
        'Pen',
        'Pen Description',
        10,
        'Education',
        '',
        '5',
        '1',
    ]
    output = []

    driver.input = mock_input
    driver.print = lambda s: output.append(s)

    driver_manager.start_admin_flow()

    driver_manager.list_product_categories()
    assert len(output) == 1
    output.clear()

    driver_manager.list_products_by_category()
    assert len(output) == 1


def test_add_product_to_user_cart(driver_manager):
    global input_values
    input_values += [
        '1',
        '10'
    ]

    driver.input = mock_input
    driver.print = lambda s: output.append(s)

    driver_manager.add_product_to_user_cart()

    driver_manager.display_cart()
    print(output)
    assert output[1] == '1. Product: Pen, Quantity: 10'


def test_place_order(driver_manager):
    global input_values, output
    input_values += [
        '1',
        'n',
    ]
    output = []

    driver.input = mock_input
    driver.print = lambda s: output.append(s)

    driver_manager.place_order()

    assert output[0] == 'Order Placed.'
    assert output[1] == 'Order Amount: 100.0, Net Payable: 100.0'


def test_admin_flow_4(driver_manager):
    global input_values, output

    input_values += [
        '4',
        '1',
        '',
        '5'
    ]
    output = []

    driver.input = mock_input
    driver.print = lambda s: output.append(s)

    driver_manager.start_admin_flow()
    print(output)
