from models import Product, Category
from base import session
from sqlalchemy.orm import exc


class ProductManager:
    def __init__(self):
        self.session = session

    def add_product(self, product_name, desc, price, category):
        try:
            new_product = Product(name=product_name, description=desc, price=price)
            self.add_category_to_product(new_product, category)
            self.save_changes(new_product)
        except Exception as e:
            print(e)

    def add_category_to_product(self, product, category):
        try:
            cat_obj = self.session.query(Category).filter(Category.name == category).one()
            product.category = cat_obj
        except exc.NoResultFound:
            raise Exception(f'Could not add product as {category} category not found')

    # def list_products_by_category(self, category):
    #     cat_obj = self.session.query(Category).filter(Category.name == category).all()
    #     for index, product in enumerate(cat_obj):
    #         print(f'{index}. {product.products}')

    def list_products(self):
        products = self.session.query(Product).all()
        return products

    def view_details(self, product_id):
        product = self.session.query(Product).get(product_id)
        return product.get_details

    def save_changes(self, changes):
        self.session.add(changes)
        self.session.commit()


# m = ProductManager()
# m.add_product('Jeep', 'Jeep Description', 9000, 'Automobiles')
# m.list_products(category='Automobiles')
# m.view_details(2)
