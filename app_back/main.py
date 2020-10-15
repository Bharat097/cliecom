from models import User
from product import ProductManager
from category import CategoryManager
from cart import CartManager
from user import UserManager
from order import OrderManager
from base import session
from sqlalchemy.orm import exc
from constants import *
import json


class Driver:
    def __init__(self):
        self.session = session
        self.logged_in = False
        self.user = None
        self.is_admin = False
        self.cart_items = None

        # self.login()

        self.category_manager = CategoryManager(session=session)
        self.cart_manager = CartManager(session=session)
        self.product_manager = ProductManager(session=session)
        self.user_manager = UserManager(session=session)
        self.order_manager = OrderManager(session=session)

    def login(self):
        email = input('Enter E-mail: ')
        pwd = input('Enter Password: ')
        try:
            user = self.session.query(User).filter_by(email=email, password=pwd).one()
            self.user = user
            self.logged_in = True
            self.is_admin = True if user.is_admin else False
            print(f'{user} logged in successfully')
        except exc.NoResultFound:
            raise Exception('wrong credentials. please try again.')

    def collect_category_details(self):
        category_detail = {}
        for key, value in CATEGORY_DETAILS.items():
            category_detail[key] = input(f'Enter {value}: ')
        return category_detail

    def collect_product_details(self):
        product_detail = {}
        for key, value in PRODUCT_DETAILS.items():
            product_detail[key] = input(f'Enter {value}: ')
        return product_detail

    def select_user(self):
        users = self.user_manager.list_users()
        for index, value in enumerate(users, 1):
            print(f'{index}. {value}')
        user_index = int(input('Select User: '))
        return users[user_index-1]

    def display_user_cart(self, user):
        cart_items = user.cart_items
        print(f'Products added to the cart by user {user}')
        for item in cart_items:
            print(f'Product: {item.product}, Quantity: {item.quantity}')
        print()

    def select_category(self):
        categories = self.category_manager.list_categories()
        for index, category in enumerate(categories, 1):
            print(f'{index}. {category}')
        category_index = int(input('Select Category: '))

        return categories[category_index-1]

    def select_product(self):
        products = self.product_manager.list_products()
        for index, product in enumerate(products, 1):
            print(f'{index}. {product}')
        product_index = int(input('Select Product: '))

        return products[product_index-1]

    def display_cart(self, action=None):
        cart_items = self.user.cart_items
        print('User\'s Cart: ')
        for index, item in enumerate(cart_items, 1):
            print(f'{index}. Product: {item.product}, Quantity: {item.quantity}')

        if action == 'select':
            item_index = int(input('Select Product: '))

            return cart_items[item_index-1]

    def place_order(self):
        items = []
        self.order_manager.create_order(self.user)
        while True:
            item = self.display_cart(action='select')
            self.order_manager.add_item(item=item.product, quantity=item.quantity)
            items.append(item)
            self.cart_manager.remove_item(product=item, silent=True, commit=False)
            add_more = input('Want to add more items from cart? (y/n)')
            if add_more not in ['y', 'Y', 'Yes', 'YES', 'yes']:
                break
        print('Order Placed.')
        res = self.order_manager.is_discount()
        if res[1]:
            print('Voila.. You got 500 discount on this order')
            print(f'Order Amount: {res[0]}, Discount: 500, Net Payable: {res[0]-500}')
        else:
            print(f'Order Amount: {res[0]}, Net Payable: {res[0]}')

        self.cart_manager.commit_changes()
        self.order_manager.complete_order()

    def is_already_added_to_cart(self, product):
        for cart_item in self.user.cart_items:
            if product.id == cart_item.product_id:
                return cart_item
        else:
            return False

    def remove_item_from_cart(self):
        item = self.display_cart(action='select')
        self.cart_manager.remove_item(product=item)

    def add_product_to_user_cart(self):
        product = self.select_product()
        quantity = int(input('Enter Quantity: '))
        cart_item = self.is_already_added_to_cart(product)
        if cart_item:
            self.cart_manager.update_item(cart_item, quantity)
        else:
            self.cart_manager.add_item(user=self.user, product=product, quantity=quantity)

    def view_product_details(self):
        product = self.select_product()
        details = self.product_manager.view_details(product_id=product.id)
        for k, v in details.items():
            print(f'{k}: {v}')

    def list_products_by_category(self):
        category = self.select_category()
        products = self.category_manager.list_products_by_category(category_name=category.name)
        for index, product in enumerate(products, 1):
            print(f'{index}. {product}')

    def list_product_categories(self):
        categories = self.category_manager.list_categories()
        for index, category in enumerate(categories, 1):
            print(f'{index}. {category}')

    def create_user(self):
        user_detail = {}
        for key, value in USER_DETAILS.items():
            user_detail[key] = input(f'Enter {value}: ')
        self.user_manager.add_user(**user_detail)

    def start_admin_flow(self):
        while True:
            print('Select option: ')
            for index, value in enumerate(ACTIONS.get('admin', []), 1):
                print(f'{index}. {value}')

            admin_choice = int(input())

            if admin_choice == 1:
                #   Add Category
                category_detail = self.collect_category_details()
                self.category_manager.add_category(**category_detail)
                input('Press Enter to Continue..')

            elif admin_choice == 2:
                #   Add Product
                product_details = self.collect_product_details()
                self.product_manager.add_product(**product_details)
                input('Press Enter to Continue..')

            elif admin_choice == 3:
                #   View Cart Details
                for_user = self.select_user()
                self.display_user_cart(for_user)
                input('Press Enter to Continue..')

            elif admin_choice == 4:
                #   View Bills
                user = self.select_user()
                bill = self.user_manager.list_bills(user=user)
                # print('Function Under Construction')
                print(json.dumps(bill, indent=4, default=str))
                input('Press Enter to Continue..')

            elif admin_choice == 5:
                return

            else:
                print('Enter Valid Input')
                input('Press Enter to Continue..')

    def start_user_flow(self):
        while True:
            print('Select option: ')
            for index, value in enumerate(ACTIONS.get('user', []), 1):
                print(f'{index}. {value}')

            user_choice = int(input())
            if user_choice == 1:
                #   List Categories
                self.list_product_categories()
                input('Press Enter to Continue..')

            elif user_choice == 2:
                #   List Products by Category
                self.list_products_by_category()
                input('Press Enter to Continue..')

            elif user_choice == 3:
                #   View Product Detail
                self.view_product_details()
                input('Press Enter to Continue..')

            elif user_choice == 4:
                #   View Cart
                self.display_cart()
                input('Press Enter to Continue..')

            elif user_choice == 5:
                #   Add Product to Cart
                self.add_product_to_user_cart()
                input('Press Enter to Continue..')

            elif user_choice == 6:
                #   Remove Product from Cart
                self.remove_item_from_cart()
                input('Press Enter to Continue..')

            elif user_choice == 7:
                #   Place Order
                self.place_order()
                input('Press Enter to Continue..')

            elif user_choice == 8:
                return

            else:
                print('Enter Valid Input')


if __name__ == '__main__':
    try:
        d = Driver()

        for i, val in enumerate(CREATE_OR_LOGIN, 1):
            print(f'{i}. {val}')
        choice = int(input())

        if choice == 1:
            d.create_user()

        if not d.logged_in:
            print('\nLog in to Account')
            d.login()

        while True:
            if d.is_admin:
                print('Select Flow')
                for i, val in enumerate(FLOW, 1):
                    print(f'{i}. {val}')
                choice = int(input())
                if choice == 1:
                    d.start_user_flow()
                elif choice == 2:
                    d.start_admin_flow()
                else:
                    print('Invalid input provided')
    except Exception as e:
        print(f'Error Occurred: {e}')
