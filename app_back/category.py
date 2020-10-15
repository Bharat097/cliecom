from models import Category, Product
# from base import session


class CategoryManager:
    def __init__(self, session):
        self.session = session

    def add_category(self, category_name):
        new_category = Category(name=category_name)

        self.save_changes(new_category)
        print(f'category {new_category} added successfully\n')

    def list_categories(self):
        categories = self.session.query(Category).order_by(Category.name).all()
        return categories

    def list_products_by_category(self, category_name):
        category_obj = self.session.query(Category).filter_by(name=category_name).one()
        return category_obj.products

    def save_changes(self, changes):
        self.session.add(changes)
        self.session.commit()
