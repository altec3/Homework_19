from flask import Flask

from project.setup.db import db
from project.setup.api import api
from project.view.auth.auth import auth_ns
from project.view.main.directors import directors_ns
from project.view.main.genres import genres_ns
from project.view.main.movies import movies_ns
from project.view.main.users import users_ns


def configure_app(application: Flask) -> None:
    db.init_app(application)
    api.init_app(application)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(movies_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(users_ns)
