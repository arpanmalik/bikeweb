from datetime import datetime
from bikeweb import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Applicant.query.get(int(user_id))

class Applicant(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstName = db.Column(db.String(20),unique=False, nullable=False)
    lastName = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.Integer(), unique=True, nullable=False)
    address = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.firstName}', '{self.lastName}','{self.phone}','{self.address}' ,'{self.email}')"

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstName = db.Column(db.String(20),unique=False, nullable=False)
    lastName = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.firstName}', '{self.lastName}','{self.email}')"


