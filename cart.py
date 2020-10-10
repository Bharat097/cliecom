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

    def remove_item(self, product):
        item = self.session.query(Cart).filter_by(product_id=product.product_id).all()
        self.save_changes(item[0], action='delete')
        print(f'product successfully removed from cart')

    def save_changes(self, changes, action='add'):
        if action == 'add':
            self.session.add(changes)
        elif action == 'delete':
            self.session.delete(changes)
        else:
            print('Invalid action specified')
        self.session.commit()

    # def list_cart_users(self):
    #     users = self.session.query(Cart.user).distinct().all()
    #     return users


# u = User('bharat', 'b@gmail.com', '1234')
# session.add(u)
# session.commit()
# u = session.query(User).filter_by(name='bharat').one()
# p = session.query(Product).filter_by(name='Jeep').one()
#
# m = CartManager(u)
# m.add_item(u, p, 1)
# m.remove_item(p)
