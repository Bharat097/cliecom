from models import Order, OrderItem, User
from base import session


class OrderManager:
    def __init__(self):
        self.session = session
        self.order = None

    def add_item(self, item, quantity):
        order_item = OrderItem(order=self.order, product=item, quantity=quantity)
        self.save_changes(order_item)

    def create_order(self, user):
        self.order = self.session.query(Order).filter_by(user=user, completed=False).first()
        if not self.order:
            self.order = Order(user=user)

    def is_discount(self):
        total = self.order.order_amount

        if total > 10000:
            return total, True
        return total, False

    def complete_order(self):
        self.order.completed = True
        self.save_changes(self.order)

    def save_changes(self, changes, action='add'):
        if action == 'add':
            self.session.add(changes)
        elif action == 'delete':
            self.session.delete(changes)
        else:
            print('Invalid action specified')
        self.session.commit()
