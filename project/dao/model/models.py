from marshmallow import Schema, fields, validate

from project.setup.db import db


# Models for SQLAlchemy and Marshmallow
class Director(db.Model):
    __tablename__ = 'director'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Director {self.name}>'


class DirectorSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=100))


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Genre {self.name}>'


class GenreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=100))


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    trailer = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey(f"{Genre.__tablename__}.id"), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey(f"{Director.__tablename__}.id"), nullable=False)

    genre = db.relationship("Genre")
    director = db.relationship("Director")

    def __repr__(self):
        return f'<Movie {self.title}>'


class MovieSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(max=255))
    description = fields.String(required=True, validate=validate.Length(max=255))
    trailer = fields.String(required=True, validate=validate.Length(max=255))
    year = fields.Integer(required=True)
    rating = fields.Integer(required=True)
    genre_id = fields.Integer(required=True)
    director_id = fields.Integer(required=True)

    genre = fields.Nested(GenreSchema)
    director = fields.Nested(DirectorSchema)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    favorite_genre = db.Column(db.Integer)
    role = db.Column(db.String(), default="user")

    def __repr__(self):
        return f'<User {self.name}>'


class UserSchema(Schema):

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(max=100))
    password = fields.String(required=True)
    favorite_genre = fields.Integer()
    role = fields.String(validate=validate.Length(max=50))
