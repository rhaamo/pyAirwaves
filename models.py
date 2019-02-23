from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_searchable import make_searchable

db = SQLAlchemy()
make_searchable(db.metadata)


class FaaMfr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icao = db.Column(db.String(10), nullable=False, unique=True)
    mfr = db.Column(db.String(255), nullable=False)
