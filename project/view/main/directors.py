from flask import request, url_for
from flask_restx import Namespace, Resource

from project.container import director_service
from project.dao.model.models import DirectorSchema
from project.helpers.decorators import auth_required, admin_required
from project.setup.api.models import error_api_model, director_api_model

directors_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@directors_ns.route("/")
class DirectorsView(Resource):
    """Shows a list of all directors"""

    @directors_ns.marshal_list_with(director_api_model, code=200, description="OK")
    @auth_required
    def get(self):
        """List all directors"""

        all_directors = director_service.get_all()
        return directors_schema.dump(all_directors), 200

    @directors_ns.expect(director_api_model)
    @directors_ns.response(201, description="OK", model=director_api_model,
                           headers={'Location': 'The URL of a newly created director'})
    @directors_ns.response(400, description="Bad Request", model=error_api_model)
    @admin_required
    def post(self):
        """Create a new director"""

        try:
            director: dict = director_schema.load(request.json)
            response = director_service.create(director)
        except Exception:
            return None, 400
        else:
            return director_schema.dump(response), 201, {'Location': url_for(
                'directors_director_view',
                did=response.id
            )}


@directors_ns.route("/<int:did>")
class DirectorView(Resource):
    """Show a single director item"""

    @directors_ns.marshal_with(director_api_model, code=200, description="OK")
    @directors_ns.response(404, description="Not Found", model=error_api_model)
    @auth_required
    def get(self, did: int):
        """Fetch a given resource"""

        director = director_service.get_by_id(did)
        return director_schema.dump(director), 200

    @directors_ns.expect(director_api_model)
    @directors_ns.response(204, description="No Content")
    @directors_ns.response(404, description="Not Found", model=error_api_model)
    @admin_required
    def put(self, did: int):
        """Update a director given its identifier"""

        data: dict = request.json
        data['id'] = did
        if director_service.update(data):
            return None, 204
        return None, 404

    @directors_ns.response(204, description="No Content")
    @directors_ns.response(404, description="Not Found")
    @admin_required
    def delete(self, did: int):
        """Delete a director given its identifier"""

        if director_service.delete(did):
            return None, 204
        return None, 404
