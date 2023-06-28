import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
db = SQLAlchemy()


def connect_to_db(app):
    # Have to run command "source config.sh"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)


class Telescope(db.Model):
    __tablename__ = "telescopes"

    telescope_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    class_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    wavelength = db.Column(JSON, nullable=False)
    temperature = db.Column(JSON, nullable=False)
    design = db.Column(db.String(255), nullable=False)
    optics = db.Column(db.String(255), nullable=False)
    fov = db.Column(JSON, nullable=False)
    instrument = db.Column(JSON, nullable=False)
    extras = db.Column(JSON, nullable=True)

    user = db.relationship("User", backref="telescopes")

    def __repr__(self):
        return f"<Telescope telescope_id={self.telescope_id} user_id={self.user_id}>"


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to db...")

'''
To add tables into the database, run 'python -i model.py' in terminal, then run
'with app.app_context():
    db.create_all()'
in interactive mode.
'''
