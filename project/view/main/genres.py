from flask import request, url_for
from flask_restx import Resource, Namespace

from project.container import genre_service
from project.dao.model.models import GenreSchema
from project.helpers.decorators import auth_required, admin_required
from project.setup.api.models import error_api_model, genre_api_model

genres_ns: Namespace = Namespace("genres")

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


@genres_ns.route("/")
class GenresView(Resource):
    """Shows a list of all genres"""

    @genres_ns.marshal_list_with(genre_api_model, code=200, description='OK')  # -> to Frontend
    @auth_required
    def get(self):
        """List all genres"""

        all_genres = genre_service.get_all()
        return genres_schema.dump(all_genres), 200

    @genres_ns.expect(genre_api_model)
    @genres_ns.response(201, description="OK", model=genre_api_model,
                        headers={'Location': 'The URL of a newly created genre'})
    @genres_ns.response(400, description="Bad Request", model=error_api_model)
    @admin_required
    def post(self):
        """Create a new genre"""

        try:
            genre: dict = genre_schema.load(request.json)
            response = genre_service.create(genre)
        except Exception:
            return None, 400
        else:
            return genre_schema.dump(response), 201, {'Location': url_for('genres_genre_view', gid=response.id)}


@genres_ns.route("/<int:gid>")
class GenreView(Resource):
    """Show a single genre item"""

    @genres_ns.marshal_with(genre_api_model, code=200, description='OK')  # -> to Frontend
    @genres_ns.response(404, description="Not Found", model=error_api_model)
    @auth_required
    def get(self, gid: int):
        """Fetch a given resource"""

        genre = genre_service.get_by_id(gid)
        return genre_schema.dump(genre), 200

    @genres_ns.expect(genre_api_model)
    @genres_ns.response(204, description="No Content")
    @genres_ns.response(404, description="Not Found", model=error_api_model)
    @admin_required
    def put(self, gid: int):
        """Update a genre given its identifier"""

        data: dict = request.json
        data['id'] = gid
        if genre_service.update(data):
            return None, 204
        return None, 404

    @genres_ns.response(204, description="No Content")
    @genres_ns.response(404, description="Not Found")
    @admin_required
    def delete(self, gid: int):
        """Delete a genre given its identifier"""

        if genre_service.delete(gid):
            return None, 204
        return None, 404
