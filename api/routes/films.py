from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from api.models import db
from api.models.film import Film
from api.schemas.film import film_schema, films_schema

# Create a "Blueprint", r model
# We can insert this into our flask app
films_router = Blueprint('films', __name__, url_prefix='/films')

# RESTful endpoints - Read
# GET requests to the collection return a list of all the actors in the database
@films_router.get('/')
def read_all_films():
    actors = Film.query.all()
    return films_schema.dump(actors)

# GET request to a specific document in the collection return a single film
@films_router.get('/<film_id>')
def read_film (film_id):
    film = Film.query.get(film_id)
    return film_schema.dump(film)

# RESTful endpoints - Create
@films_router.post('/')
def create_film():
    film_data = request.json           # Get the parsed request body

    try:
        film_schema.load(film_data)   # Validate against the schema
    except ValidationError as err:
        return jsonify(err.messages), 400

    film = Film(**film_data)         # Create new actor model
    db.session.add(film)               # Insert the record
    db.session.commit()                 # Update the database

    return film_schema.dump(film)    # Serialize the created actor
