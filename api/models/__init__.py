from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .actor import Actor
from .film import Film
from .film_actor import film_actor