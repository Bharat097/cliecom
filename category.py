from models import Category, Product
from base import session


class CategoryManager:
    def __init__(self):
        self.session = session

    def add_category(self, category_name):
        new_category = Category(name=category_name)

        self.save_changes(new_category)

    def list_categories(self):
        categories = self.session.query(Category).order_by(Category.name).all()
        return categories

    def list_products_by_category(self, category_name):
        category_obj = self.session.query(Category).filter_by(name=category_name).one()
        return category_obj.products

    def save_changes(self, changes):
        self.session.add(changes)
        self.session.commit()


if __name__ == '__main__':
    c = CategoryManager()
    # c.list_categories()
    # c.list_products_by_category(category_name='Automobiles')
    # c.add_category('Electronics')
    # c.add_category('Men')
    # c.add_category('Women')
    # c.add_category('Automobiles')
    # c.add_category('Education')
    # c.add_category('Sports')
