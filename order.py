from models import Order, OrderItem
from base import session


class OrderManager:
    def __init__(self, user):
        self.session = session
        self.order = Order(user=user)

    def add_item(self, item, quantity):
        order_item = OrderItem(order=self.order, product=item, quantity=quantity)
        self.save_changes(order_item)

    def save_changes(self, changes, action='add'):
        if action == 'add':
            self.session.add(changes)
        elif action == 'delete':
            self.session.delete(changes)
        else:
            print('Invalid action specified')
        self.session.commit()
