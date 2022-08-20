import os


class Config:

    DEBUG = True

    # SQL settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'project/movies.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # For correct display of Cyrillic fonts
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    RESTX_JSON = {'ensure_ascii': False}

    # To fill the database
    DIRECTORS_DATA = "project/setup/db/fixtures/directors.json"
    GENRES_DATA = "project/setup/db/fixtures/genres.json"
    MOVIES_DATA = "project/setup/db/fixtures/movies.json"

    # For paginate
    ITEMS_PER_PAGE = 10
