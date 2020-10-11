from models import User
from base import session
# from sqlalchemy.orm import exc


class UserManager:
    def __init__(self):
        self.session = session

    def add_user(self, name, email, password):
        new_user = User(name=name, email=email, password=password)
        self.save_changes(new_user)

    def list_users(self):
        users = self.session.query(User).all()
        return users

    def list_bills(self, user):
        orders = user.orders
        bill = {}
        for order in orders:
            item_list = {}
            items = order.order_items
            for item in items:
                item_list[item.product.name] = item.quantity
            bill[order.id] = {
                'total_amount': order.order_amount,
                'time': order.created,
                'items': item_list
            }

        return bill

    def save_changes(self, changes):
        self.session.add(changes)
        self.session.commit()
