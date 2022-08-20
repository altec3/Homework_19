from project.dao.main.genre import GenreDAO


class GenreService:

    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def create(self, data: dict):
        return self.dao.create(data)

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, gid: int):
        return self.dao.get_by_id(gid)

    def update(self, data: dict) -> bool:
        return self.dao.update(data)

    def delete(self, gid: int) -> bool:
        return self.dao.delete(gid)
