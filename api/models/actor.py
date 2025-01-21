from api.models import db
from api.models.film_actor import film_actor


# A model of out actor table
class Actor(db.Model):
    __tablename__ = 'actor'
    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    films = db.relationship(
        'Film',
        secondary=film_actor,
        back_populates='actors'
    )
