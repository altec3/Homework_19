from flask import request, current_app as app, url_for
from flask_restx import Resource, Namespace

from project.container import movie_service
from project.dao.model.models import MovieSchema
from project.helpers.decorators import auth_required, admin_required
from project.setup.api.models import movie_api_model, error_api_model
from project.setup.api.parsers import page_parser, movie_filter_and_page_parser

movies_ns: Namespace = Namespace("movies")

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()


@movies_ns.route("/")
class MoviesView(Resource):
    """Shows a list of all movies, and lets you POST to add new movies"""

    @movies_ns.expect(movie_filter_and_page_parser)  # <- from Frontend
    @movies_ns.marshal_list_with(movie_api_model, code=200, description='OK')  # -> to Frontend
    @auth_required
    def get(self):
        """List all movies"""

        page = request.args.get("page", 1, type=int)
        fields = {}

        if request.args.get("director_id"):
            fields["director_id"] = int(request.args.get("director_id"))
        if request.args.get("genre_id"):
            fields["genre_id"] = int(request.args.get("genre_id"))
        if request.args.get("year"):
            fields["year"] = int(request.args.get("year"))

        if fields:
            movies = movie_service.get_by_fields(page, app.config.get("ITEMS_PER_PAGE"), fields)
        else:
            movies = movie_service.get_all(page, app.config.get("ITEMS_PER_PAGE"))
        return movies_schema.dump(movies), 200

    @movies_ns.expect(movie_api_model)
    @movies_ns.response(201, description="OK", model=movie_api_model,
                        headers={'Location': 'The URL of a newly created movie'})
    @movies_ns.response(404, description="Not Found", model=error_api_model)
    @admin_required
    def post(self):
        """Create a new movie"""

        try:
            movie: dict = movie_schema.load(request.json)
            response = movie_service.create(movie)
        except Exception:
            return None, 400
        else:
            return movie_schema.dump(response), 201, {'Location': url_for('movies_movie_view', mid=response.id)}


@movies_ns.route("/<int:mid>")
class MovieView(Resource):
    """Show a single movie item and lets you delete them"""

    @movies_ns.expect(page_parser)
    @movies_ns.marshal_with(movie_api_model, code=200, description='OK')
    @movies_ns.response(404, description="Not Found", model=error_api_model)
    @auth_required
    def get(self, mid: int):
        """Fetch a given resource"""

        movie = movie_service.get_by_id(mid)
        return movie_schema.dump(movie), 200

    @movies_ns.expect(movie_api_model)
    @movies_ns.response(204, description="No Content")
    @movies_ns.response(404, description="Not Found", model=error_api_model)
    @admin_required
    def put(self, mid: int):
        """Update a movie given its identifier"""

        data: dict = request.json
        data['id'] = mid
        if movie_service.update(data):
            return None, 204
        return None, 404

    @movies_ns.response(204, description="No Content")
    @movies_ns.response(404, description="Not Found")
    @admin_required
    def delete(self, mid: int):
        """Delete a movie given its identifier"""

        if movie_service.delete(mid):
            return None, 204
        return None, 404
