from flask import Flask

from project.dao.model.models import Director, Genre, Movie
from project.setup.db import db
from utils import load_json


def fill_db(application: Flask) -> None:
    """Заполняет таблицы базы (director, genre, movie) данными

    :param application: Flask app
    :return: None
    """

    directors_data = load_json(application.config.get("DIRECTORS_DATA"))
    genres_data = load_json(application.config.get("GENRES_DATA"))
    movies_data = load_json(application.config.get("MOVIES_DATA"))

    with db.session.begin():
        for item in directors_data:
            db.session.add(Director(**item))
        for item in genres_data:
            db.session.add(Genre(**item))
        for item in movies_data:
            db.session.add(Movie(**item))


def create_db(application: Flask) -> None:
    """ Создает базу

    :param application: Flask app
    :return: None
    """
    with application.app_context():
        db.drop_all()
        db.create_all()
