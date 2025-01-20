from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from api.models import db
from api.models.actor import Actor
from api.schemas.actor import actor_schema, actors_schema

# Create a "Blueprint", or model
# We can insert this into our flask app
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

    return actor_schema.dump(actor)    # Serialize the created actor

# Update an actors record
@actors_router.put('/<actor_id>')
def update_actor(actor_id):
    actor = Actor.query.get(actor_id)
    actor_data = request.json

    if actor is None:
        return jsonify({'message': 'Actor not found'}), 404. # TODO: add errors like this to all potential outcomes

    try:
        actor_schema.load(actor_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in actor_data.items():
        setattr(actor, key, value)
    db.session.commit()

    return actor_schema.dump(actor)

# Delete an actors record

@actors_router.delete('/<actor_id>')
def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)

    if actor is None:
        return jsonify({'message': 'Actor not found'}), 404

    db.session.delete(actor)
    db.session.commit()
    return jsonify({'message': 'Actor deleted successfully'}), 200

