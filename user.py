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

    def save_changes(self, changes):
        self.session.add(changes)
        self.session.commit()
