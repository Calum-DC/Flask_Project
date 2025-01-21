from api.models import db
from api.models.film_actor import film_actor

# Model of the film table
class Film(db.Model):
    __tablename__ = 'film'
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    release_year = db.Column(db.String(255), nullable=False)
    actors = db.relationship(
        'Actor',
        secondary=film_actor,
        back_populates='films'
    )




