from flask import request, current_app as app, url_for
from flask_restx import Resource, Namespace

from project.container import user_service
from project.dao.model.models import UserSchema
from project.setup.api.parsers import page_parser
from project.setup.api.models import user_api_model, error_api_model
from project.helpers.decorators import admin_required

users_ns: Namespace = Namespace("users")

users_schema = UserSchema(many=True)
user_schema = UserSchema()


@users_ns.route("/")
class UsersView(Resource):
    """Shows a list of all user, and lets you POST to add new users"""

    @users_ns.expect(page_parser)
    @users_ns.marshal_list_with(user_api_model, code=200, description='OK')  # -> to Frontend
    @admin_required
    def get(self):
        """List all users"""

        page = request.args.get("page", 1, type=int)
        users = user_service.get_all(page, app.config.get("ITEMS_PER_PAGE"))
        return users_schema.dump(users), 200

    @users_ns.expect(user_api_model)
    @users_ns.response(201, description="OK", model=user_api_model,
                       headers={'Location': 'The URL of a newly created movie'})
    @users_ns.response(404, description="Not Found", model=error_api_model)
    def post(self):
        """Register a new user"""

        try:
            user: dict = user_schema.load(request.json)

            response = user_service.create(user)
        except Exception:
            return None, 400
        else:
            return user_schema.dump(response), 201, {'Location': url_for('movies_movie_view', mid=response.id)}


@users_ns.route("/<int:uid>")
class UserView(Resource):
    """Show a single user item and lets you delete them"""

    @users_ns.marshal_with(user_api_model, code=200, description='OK')
    @users_ns.response(404, description="Not Found", model=error_api_model)
    @admin_required
    def get(self, uid: int):
        """Fetch a given resource"""

        user = user_service.get_by_id(uid)
        return user_schema.dump(user), 200

    @users_ns.expect(user_api_model)
    @users_ns.response(204, description="No Content")
    @users_ns.response(404, description="Not Found", model=error_api_model)
    @admin_required
    def put(self, uid: int):
        """Update a user given its identifier"""

        data: dict = request.json
        data['id'] = uid
        if user_service.update(data):
            return None, 204
        return None, 404

    @users_ns.response(204, description="No Content")
    @users_ns.response(404, description="Not Found")
    @admin_required
    def delete(self, uid: int):
        """Delete a user given its identifier"""

        if user_service.delete(uid):
            return None, 204
        return None, 404
