from project.dao.model.models import User

from flask_sqlalchemy import SQLAlchemy


class UserDAO:

    def __init__(self, session: SQLAlchemy().session):
        self._session = session

    def create(self, data: dict) -> User:
        user = User(**data)
        self._session.add(user)
        self._session.commit()

        return user

    def get_all(self, page: int, per_page: int) -> list[User]:
        return self._session.query(User).paginate(page, per_page, False).items

    def get_by_id(self, uid: int) -> User:
        return self._session.query(User).get_or_404(uid)

    def get_by_username(self, username: str) -> User:
        return self._session.query(User).filter(User.username == username).first_or_404()

    def update(self, data: dict) -> bool:
        uid = data.get('id')
        if self._session.query(User).filter(User.id == uid).update(data):
            self._session.commit()
            return True

        return False

    def delete(self, uid: int) -> bool:
        if self._session.query(User).filter(User.id == uid).delete():
            self._session.commit()
            return True

        return False
