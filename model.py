
from sqlalchemy.dialects.postgresql import JSON
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User username={self.username}>"

    def get_id(self):
        return self.user_id


class Telescope(db.Model):
    __tablename__ = "telescopes"

    telescope_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    telescope_name = db.Column(db.String(255), nullable=False)
    class_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    wavelength = db.Column(JSON, nullable=False)
    temperature = db.Column(JSON, nullable=False)
    design = db.Column(db.String(255), nullable=False)
    optics = db.Column(db.String(255), nullable=False)
    fov = db.Column(JSON, nullable=False)
    instrument = db.Column(JSON, nullable=False)
    extras = db.Column(JSON, nullable=True)
    cost = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", backref="telescopes")

    def __repr__(self):
        return f"<Telescope telescope_id={self.telescope_id} user_id={self.user_id}>"
