from project.service.reg import RegService
from project.setup.db import db
from project.dao.main.director import DirectorDAO
from project.dao.main.genre import GenreDAO
from project.dao.main.movie import MovieDAO
from project.dao.main.user import UserDAO
from project.service.director import DirectorService
from project.service.genre import GenreService
from project.service.movie import MovieService
from project.service.user import UserService
from project.service.auth import AuthService


director_dao = DirectorDAO(db.session)
director_service = DirectorService(director_dao)

genre_dao = GenreDAO(db.session)
genre_service = GenreService(genre_dao)

movie_dao = MovieDAO(db.session)
movie_service = MovieService(movie_dao)

user_dao = UserDAO(db.session)
reg_service = RegService()
user_service = UserService(user_dao, reg_service)

auth_service = AuthService(user_service)
