from models import Cart
from base import session


class CartManager:
    def __init__(self):
        self.session = session

    def add_item(self, user, product, quantity):
        item = Cart(user=user, product=product, quantity=quantity)
        self.save_changes(item)
        print(f'product: {product} successfully added to cart')

    def update_item(self, item, quantity):
        item.quantity += quantity
        self.save_changes(item)

    def remove_item(self, product, silent=False, commit=True):
        item = self.session.query(Cart).filter_by(product_id=product.product_id).all()
        self.save_changes(item[0], action='delete', commit=commit)
        if not silent:
            print(f'product successfully removed from cart')

    def save_changes(self, changes, action='add', commit=True):
        if action == 'add':
            self.session.add(changes)
        elif action == 'delete':
            self.session.delete(changes)
        else:
            print('Invalid action specified')
        if commit:
            self.session.commit()

    def commit_changes(self):
        self.session.commit()
