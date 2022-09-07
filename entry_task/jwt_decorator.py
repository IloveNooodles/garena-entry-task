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
            # token = request.headers["Authorization"]
            # token = decode_jwt(token)
            # logger.log().info("User Autohrized")
            # request.session["token"] = token
            # request.session.set_expiry(7200)
            request_body = json.loads(request.body) 
            token = request_body["token"]
            decode_jwt(token)
            request.session["token"] = token
            request.session.set_expiry(7200)
            logger.log().info("User Autohrized")
            return func(request, *args, **kwargs)
        except Exception as e:
            logger.log().error(str(e))
            return JsonResponse({
              "Status": "Error",
              "Message": "Unauthorized"
            }, status=HTTPStatus.UNAUTHORIZED)

    return wrapper


def decode_jwt(token):
    jwtInstance = JWTAuth()
    decoded_token = jwtInstance.decode(token)
    return decoded_token