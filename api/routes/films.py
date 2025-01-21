from flask import Blueprint, request, jsonify, render_template
from marshmallow import ValidationError

from api.models import db, Film
from api.schemas.film import film_schema, films_schema

# Create a "Blueprint"
films_router = Blueprint('films_router', __name__, url_prefix='/films')

# GET requests to the collection return a list of all the films in the database
@films_router.get('/')
def read_all_films():
    page = request.args.get('page', 1, type=int)
    per_page = 30
    pagination = Film.query.paginate(page=page, per_page=per_page)
    films = pagination.items
    return render_template('films.html', films=films, pagination=pagination)

# GET request to a specific document in the collection return a single film
@films_router.get('/<film_id>')
def read_film (film_id):
    film = Film.query.get(film_id)
    return render_template('film.html', film=film)



# Create new film and relevant details
@films_router.post('/')
def create_film():
    film_data = request.json

    try:
        film_schema.load(film_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    film = Film(**film_data)
    db.session.add(film)
    db.session.commit()

    return film_schema.dump(film)

# Update a film file
@films_router.put('/<film_id>')
def update_film(film_id):
    film = Film.query.get(film_id)
    film_data = request.json

    if film is None:
        return jsonify({'message': 'Film not found'}), 404.
    try:
        film_schema.load(film_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in film_data.items():
        setattr(film, key, value)
    db.session.commit()

    return film_schema.dump(film)

# Delete a film record
@films_router.delete('/<film_id>')
def delete_film(film_id):
    film = Film.query.get(film_id)

    if film is None:
        return jsonify({'message': 'Film not found'}), 404

    db.session.delete(film)
    db.session.commit()
    return jsonify({'message': 'Film deleted successfully'}), 200

# find all the actors in a specified film
@films_router.get('/<film_id>/actors')
def get_actors_by_film(film_id):
    # Fetch the actor by ID
    film = Film.query.get(film_id)

    # Access related films using the `films` relationship
    actors = film.actors

    # Serialize the results
    actors_data = [
        {"actor_id": actor.actor_id, "first_name": actor.first_name, "last_name": actor.last_name}
        for actor in actors
    ]

    # # Return the film title at the top
    # return { "actors": actors_data, "title": film.title,}

    return render_template("actors_in_film.html", title=film.title, id=film.film_id, actors=actors_data)


# add film to actor
