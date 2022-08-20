from flask import request
from flask_restx import Namespace, Resource

from project.container import auth_service
from project.setup.api.models import tokens_api_model, error_api_model
from project.setup.api.parsers import auth_parser, refresh_auth_parser

auth_ns: Namespace = Namespace("auth")


@auth_ns.route("/")
class AuthsView(Resource):

    @auth_ns.expect(auth_parser)
    @auth_ns.marshal_list_with(tokens_api_model, code=201, description='OK')
    @auth_ns.response(400, description="Bad Request", model=error_api_model)
    @auth_ns.response(404, description="No Found", model=error_api_model)
    def post(self):
        """User authentication"""

        data: dict = request.json

        return auth_service.generate_tokens(data), 201

    @auth_ns.expect(refresh_auth_parser)
    @auth_ns.marshal_list_with(tokens_api_model, code=201, description='OK')
    @auth_ns.response(400, description="Bad Request", model=error_api_model)
    def put(self):
        """Update user authentication"""

        data: dict = request.json

        return auth_service.approve_refresh_token(data), 201
