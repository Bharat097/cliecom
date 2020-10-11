from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from base import Base, engine
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    name = Column(String(length=20))
    password = Column(String)
    is_admin = Column(Boolean, default=True)

    cart_items = relationship('Cart', back_populates='user')
    orders = relationship('Order', back_populates='user')

    def __init__(self, name, email, password):
        self.email = email
        self.name = name
        self.password = password

    def __repr__(self):
        return self.name


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=20))
    description = Column(String(length=200))
    price = Column(Float(precision=2))
    category_id = Column(Integer, ForeignKey('categories.id'))

    carts = relationship('Cart', back_populates='product')
    category = relationship('Category', back_populates='products')

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    # def add_category(self, category):
    #     self.category = category

    @property
    def get_details(self):
        details = {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category
        }

        return details

    def __repr__(self):
        return self.name


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=20))

    products = relationship('Product', back_populates='category')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    product = relationship('Product', back_populates='carts')
    user = relationship('User', back_populates='cart_items')

    def __init__(self, quantity, user, product):
        self.quantity = quantity
        self.user = user
        self.product = product


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    completed = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow())

    order_items = relationship('OrderItem', back_populates='order')
    user = relationship('User', back_populates='orders')

    def __init__(self, user=user, completed=False, created=datetime.utcnow()):
        self.completed = completed
        self.created = created
        self.user = user

    @property
    def order_amount(self):
        total = 0
        items = self.order_items

        for item in items:
            total += (item.product.price * item.quantity)

        return total


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    order = relationship('Order', back_populates='order_items')
    product = relationship('Product')

    def __init__(self, order, product, quantity):
        self.quantity = quantity
        self.order = order
        self.product = product


if __name__ == '__main__':
    Base.metadata.create_all(engine)
