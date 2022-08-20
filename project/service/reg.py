import base64
import hashlib
import hmac

from project.helpers.constants import PWD_SALT, PWD_ITERATIONS


class RegService:

    def generate_password(self, password: str) -> bytes:
        hash_digest = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=PWD_SALT,
            iterations=PWD_ITERATIONS,
        )

        return base64.b64encode(hash_digest)
