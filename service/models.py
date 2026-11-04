"""Account model"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DataValidationError(Exception):
    """Raised when data is missing or invalid"""


def init_db(app):
    """Initialize the database"""
    db.init_app(app)
    app.app_context().push()
    db.create_all()


class Account(db.Model):
    """Class that represents an Account"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256))
    phone_number = db.Column(db.String(32))

    def create(self):
        """Creates an Account in the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates an Account in the database"""
        db.session.commit()

    def delete(self):
        """Removes an Account from the database"""
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes an Account into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
        }

    def deserialize(self, data):
        """Sets attributes from a dictionary"""
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data.get("address")
            self.phone_number = data.get("phone_number")
        except (KeyError, TypeError) as error:
            raise DataValidationError("Invalid account data: " + str(error)) from error
        return self

    @classmethod
    def all(cls):
        """Returns all Accounts"""
        return cls.query.all()

    @classmethod
    def find(cls, account_id):
        """Finds an Account by its id"""
        return cls.query.get(account_id)
