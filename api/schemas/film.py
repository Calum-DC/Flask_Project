from api.models.film import Film
from api.schemas import ma

# Auto generate a schema for Actor models
# We can use this to serialize and validate actor data

class FilmSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Film
        ordered = True

# Instantiate the schema for both a single actor and many actors
film_schema = FilmSchema()
films_schema = FilmSchema(many=True)