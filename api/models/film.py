from api.models import db

# Model of the film table
class Film(db.Model):
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    release_year = db.Column(db.String(255), nullable=False)
    # language_id = db.Column(db.Integer, nullable=False)



