from app import db
from models import User

class UserRepository:

    def get_all(self):
        return User.query.all()

    def create(self, name, email, password):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user