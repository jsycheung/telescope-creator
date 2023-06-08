import os
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_to_db(app):
    # Have to run command "source config.sh"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

# Run command in postgres
'''
CREATE TABLE telescopes (
    id SERIAL PRIMARY KEY,
    class_name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    wavelength VARCHAR(255) NOT NULL,
    design VARCHAR(255) NOT NULL,
    optics VARCHAR(255) NOT NULL,
    fov VARCHAR(255) NOT NULL,
    instrument VARCHAR(255) NOT NULL,
    extras VARCHAR(255) NOT NULL
);
'''

class Telescope(db.Model):
    __tablename__ = "telescopes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    wavelength = db.Column(db.String(255), nullable=False)
    design = db.Column(db.String(255), nullable=False)
    optics = db.Column(db.String(255), nullable=False)
    fov = db.Column(db.String(255), nullable=False)
    instrument = db.Column(db.String(255), nullable=False)
    extras = db.Column(db.String(255), nullable=True)

    def __init__(self, class_name, location, wavelength, design, optics, fov, instrument, extras):
        self.class_name = class_name
        self.location = location
        self.wavelength = wavelength
        self.design = design
        self.optics = optics
        self.fov = fov
        self.instrument = instrument
        self.extras = extras


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to db...")