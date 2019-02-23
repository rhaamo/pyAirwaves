from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_searchable import make_searchable

db = SQLAlchemy()
make_searchable(db.metadata)


# #### Base ####
