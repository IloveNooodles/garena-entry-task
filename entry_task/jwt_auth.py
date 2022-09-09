import environ
import jwt

env = environ.Env()
environ.Env().read_env()


class JWTAuth:
    def __init__(self):
        self.secret = env("JWT_SECRET")

    def encode(self, payload):
        token = jwt.encode(payload=payload, key=self.secret, algorithm="HS256")
        return token

    def decode(self, token):
        decoded_token = jwt.decode(
            jwt=token.encode("latin-1"), key=self.secret, algorithms="HS256"
        )
        return decoded_token
