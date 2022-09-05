import environ
import jwt

env = environ.Env()
environ.Env().read_env()


class JWTAuth:
    def __init__(self):
        self.secret = env("JWT_SECRET")

    def encode(self, payload):
        token = jwt.encode(payload=payload, key=self.secret, algorithm="HS256")
        encoded_token = token.encode("latin-1")
        return encoded_token

    def decode(self, token):
        decoded_token = jwt.decode(jwt=token, key=self.secret, algorithms="HS256")
        return decoded_token
