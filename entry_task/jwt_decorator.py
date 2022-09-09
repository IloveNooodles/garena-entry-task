from functools import wraps
from entry_task.jwt_auth import JWTAuth
from http import HTTPStatus
from django.http import JsonResponse
from entry_task.logger import Logger
import json


def auth(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        logger = Logger("auth_middleware")
        try:
            # Ini kalo di header
            auth_header = request.headers["Authorization"]
            token = auth_header.split(" ")[1]
            decoded_token = decode_jwt(token)
            request.user = decoded_token
            logger.log().info("User Autohrized")
            return func(request, *args, **kwargs)
        except Exception as e:
            logger.log().error(str(e))
            return JsonResponse(
                {"Status": "Error", "Message": "Unauthorized"},
                status=HTTPStatus.UNAUTHORIZED,
            )

    return wrapper


def decode_jwt(token):
    jwtInstance = JWTAuth()
    decoded_token = jwtInstance.decode(token)
    return decoded_token
