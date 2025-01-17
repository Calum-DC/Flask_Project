from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from api.models import db
from api.models.actor import Actor
from api.schemas.actor import actor_schema, actors_schema

# Create a "Blueprint", or model
# We can inster this into our flask app
actors_router = Blueprint('actors', __name__, url_prefix='/actors')


# RESTful endpoints - Read
# GET requests to the collection return a list of all the actors in the database
@actors_router.get('/')
def read_all_actors():
    actors = Actor.query.all()
    return actors_schema.dump(actors)

# GET request to a specific documet in the collection return a single actor
@actors_router.get('/<actor_id>')
def read_actor(actor_id):
    actor = Actor.query.get(actor_id)
    return actor_schema.dump(actor)

# RESTful endpoints - Create
@actors_router.post('/')
def create_actor():
    actor_data = request.json           # Get the parsed request body

    try:
        actor_schema.load(actor_data)   # Validate against the schema
    except ValidationError as err:
        return jsonify(err.messages), 400

    actor = Actor(**actor_data)         # Create new actor model
    db.session.add(actor)               # Insert the record
    db.session.commit()                 # Update the database

    return actors_schema.dump(actor)    # Serialize the created actor



