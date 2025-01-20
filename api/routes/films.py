from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from api.models import db
from api.models.film import Film
from api.schemas.film import film_schema, films_schema

# Create a "Blueprint", or model
# We can insert this into our flask app
films_router = Blueprint('films', __name__, url_prefix='/films')

# RESTful endpoints - Read
# GET requests to the collection return a list of all the actors in the database
@films_router.get('/')
def read_all_films():
    actors = Film.query.all()
    return films_schema.dump(actors)

