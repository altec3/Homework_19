import base64
import calendar
import datetime
import hashlib
import hmac

import jwt
from flask import abort

from project.helpers.constants import JWT_ALG, JWT_SECRET, PWD_SALT, PWD_ITERATIONS
from project.service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def generate_tokens(self, auth_data: dict, is_refresh: bool = False) -> dict:
        username = auth_data.get("username", None)
        password = auth_data.get("password", None)

        user = self._user_service.get_by_username(username)

        if not is_refresh:
            if not self.compare_passwords(user.password, password):
                abort(400)

        data = {
            "username": user.username,
            "role": user.role,
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALG)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALG)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def approve_refresh_token(self, auth_data: dict):
        refresh_token = auth_data.get("refresh_token")
        data: dict = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALG])

        return self.generate_tokens(data, is_refresh=True)

    def compare_passwords(self, password_hash: bytes, other_password: str) -> bool:
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac(
                hash_name="sha256",
                password=other_password.encode("utf-8"),
                salt=PWD_SALT,
                iterations=PWD_ITERATIONS,
            )
        )
