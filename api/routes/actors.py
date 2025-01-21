from flask import Blueprint, request, jsonify, render_template
from marshmallow import ValidationError

from api.models import db, Actor
from api.schemas.actor import actor_schema, actors_schema

# Create a "Blueprint", or model
# We can insert this into our flask app
actors_router = Blueprint('actors_router', __name__, url_prefix='/actors')

# GET requests to the collection return a list of all the actors in the database
@actors_router.get('/')
def read_all_actors():
    page = request.args.get('page', 1, type=int)
    per_page = 30
    pagination = Actor.query.paginate(page=page, per_page=per_page)
    actors = pagination.items
    return render_template('actors.html', actors=actors, pagination=pagination)

# GET request to a specific document in the collection return a single actor
@actors_router.get('/<actor_id>')
def read_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    return render_template('actor.html', actor=actor)

# Create a new actor and save output
@actors_router.post('/')
def create_actor():
    actor_data = request.json

    try:
        actor_schema.load(actor_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    actor = Actor(**actor_data)
    db.session.add(actor)
    db.session.commit()

    return actor_schema.dump(actor)

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

# find all the films by a specified actor
@actors_router.get('/<actor_id>/films')
def get_films_by_actor(actor_id):
    # Fetch the actor by ID
    actor = Actor.query.get(actor_id)

    # Access related films using the `films` relationship
    films = actor.films

    # Serialize the results
    films_data = [film.title for film in films]

    return {"actor_id": actor.actor_id, "films": films_data}







