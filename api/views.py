from datetime import datetime, timedelta
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.cache import cache
from entry_task.logger import Logger
from entry_task.hash import HashPassword
from entry_task.jwt_auth import JWTAuth
from entry_task.jwt_decorator import auth, decode_jwt
from entry_task.utils import is_valid_body
from http import HTTPStatus
from api.models import User
from api.utils import (
    validate_email,
    response_error,
    response_success,
    get_username_from_session,
)
import json
import requests
import uuid

URL = "https://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json"
TIMEOUT = 3600  # in second
CACHE_TTL = getattr(settings, "CACHE_TTL", TIMEOUT)


@require_http_methods(["POST"])
@csrf_exempt
def register(request):
    logger = Logger("register")
    if (
        request.method == "POST"
        and request.headers["Content-Type"] == "application/json"
    ):
        request_body = json.loads(request.body)
        keys_to_check = ["username", "password", "email", "name"]

        # check all the field
        if not is_valid_body(request_body, keys_to_check):
            logger.log().error("Incomplete request body")
            return response_error(
                HTTPStatus.BAD_REQUEST, "Please fill the request body correctly"
            )

        # find user by ref code
        referred_user = None
        if "ref_code" in request_body:
            referred_user = User.find_user_by_ref(User, request_body["ref_code"])

        if not referred_user and "ref_code" in request_body:
            logger.log().error("Invalid referral code")
            return response_error(
                HTTPStatus.NOT_FOUND, "No user found with inputted referral code"
            )

        # Username validation
        if User.find_user_by_username(User, username=request_body["username"]):
            logger.log().error("Username is already exists")
            return response_error(HTTPStatus.CONFLICT, "Username is already exists")

        # Email validation
        is_valid = validate_email(request_body["email"])
        if not is_valid:
            logger.log().error("Email is invalid")
            return response_error(
                HTTPStatus.UNPROCESSABLE_ENTITY, "Please provide correct email"
            )

        # Hash Password
        hashInstance = HashPassword(request_body["password"])
        hashed_password = hashInstance.hash()

        # random ref_code
        referral_code = str(uuid.uuid4())

        # Create user
        user_to_add = User(
            username=request_body["username"],
            password=hashed_password,
            name=request_body["name"],
            email=request_body["email"],
            referal_code=referral_code,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        if referred_user:
            user_to_add.referred_by = referred_user

        user_to_add.save()
        response = request_body
        response.pop("password")
        return response_success(
            "Successfuly create new user", response, status=HTTPStatus.CREATED
        )

    logger.log().error("Invalid method access")
    return response_error(HTTPStatus.METHOD_NOT_ALLOWED, "Method not allowed")


@require_http_methods(["POST"])
@csrf_exempt
def login(request):
    logger = Logger("login")
    if (
        request.method == "POST"
        and request.headers["Content-Type"] == "application/json"
    ):
        request_body = json.loads(request.body)
        keys_to_check = ["username", "password"]
        # Payload validation
        if not is_valid_body(request_body, keys_to_check):
            logger.log().error("Incomplete request body")
            return response_error(
                HTTPStatus.BAD_REQUEST, "Please fill the request body correctly"
            )

        # Check for matching username
        user = User.find_user_by_username(User, request_body["username"])

        if not user:
            logger.log().error("No user found ")
            return response_error(HTTPStatus.NOT_FOUND, "No user found")

        # Check for password
        hashInstance = HashPassword(request_body["password"])
        is_matched = hashInstance.check(user.password)

        if not is_matched:
            logger.log().error("Password didn't match")
            return response_error(HTTPStatus.UNPROCESSABLE_ENTITY, "Incorrect Password")

        # Send the JWT
        exp_date = datetime.now() + timedelta(hours=2)
        payload = {
            "username": request_body["username"],
            "ref_code": user.referal_code,
            "id": user.id,
            "name": user.name,
            "exp": exp_date,
        }

        jwtInstance = JWTAuth()
        token = jwtInstance.encode(payload)

        logger.log().info("Successfuly login")
        return response_success("Successfuly login", {"Token": token})

    logger.log().error("Method not allowed")
    return response_error(HTTPStatus.METHOD_NOT_ALLOWED, "Method not allowed")


@require_http_methods(["PUT"])
@csrf_exempt
@auth
def edit_profile(request):
    logger = Logger("edit_profile")
    if (
        request.method == "PUT"
        and request.headers["Content-Type"] == "application/json"
    ):
        request_body = json.loads(request.body)

        # Get info user from request
        username = request.user["username"]
        print(request.user)
        selected_user = User.find_user_by_username(User, username)
        if not selected_user:
            logger.log().error("No user found ")
            return response_error(HTTPStatus.NOT_FOUND, "No user found")

        # If user want to change username
        if "username" in request_body:
            if User.find_user_by_username(User, username=request_body["username"]):
                logger.log().error("Username is already exists")
                return response_error(HTTPStatus.CONFLICT, "Username is already exists")

            selected_user.username = request_body["username"]

        # Change name
        if "name" in request_body:
            selected_user.name = request_body["name"]

        # Change email
        if "email" in request_body:
            is_email_valid = validate_email(request_body["email"])
            if not is_email_valid:
                logger.log().error("Email is invalid")
                return response_error(
                    HTTPStatus.UNPROCESSABLE_ENTITY, "Please provide correct email"
                )

            selected_user.email = request_body["email"]

        # Save and send response
        selected_user.save()
        logger.log().error("Successfuly edit user")
        response = request_body
        return response_success("Successfuly Edit User", response)
    logger.log().info("Method not allowed")
    return response_error(HTTPStatus.METHOD_NOT_ALLOWED, "Method not allowed")


@require_http_methods(["POST"])
@csrf_exempt
@auth
def input_ref(request):
    logger = Logger("find_user")
    if (
        request.method == "POST"
        and request.headers["Content-Type"] == "application/json"
    ):
        request_body = json.loads(request.body)
        if "ref_code" not in request_body:
            logger.log().error("Referal code is empty")
            return response_error(HTTPStatus.BAD_REQUEST, "referal code is empty")

        # Get User Info
        username = request.user["username"]
        selected_user = User.find_user_by_username(User, username)

        if not selected_user:
            logger.log().error("No user found ")
            return response_error(HTTPStatus.NOT_FOUND, "No user found")

        # if already input referral code
        if selected_user.referred_by:
            logger.log().error("User already entered referral code")
            return response_error(
                HTTPStatus.BAD_REQUEST, "Referral code is already entered"
            )

        # Search user by ref code
        referred_by = User.find_user_by_ref(User, request_body["ref_code"])

        if not referred_by:
            logger.log().error("No user found with that referral code")
            return response_error(
                HTTPStatus.NOT_FOUND, "No user found with referral code"
            )

        # Check if its the same id
        if referred_by.username == selected_user.username:
            logger.log().error("You can't refer yourself")
            return response_error(HTTPStatus.BAD_REQUEST, "You can't refer yourself")

        # Save and send response
        selected_user.referred_by = referred_by
        selected_user.save()
        logger.log().error("Successfuly input referral code")
        response = request_body
        response.pop("token")
        return response_success("Successfuly input referral code", response)

    logger.log().error("Method not allowed")
    return response_error(HTTPStatus.METHOD_NOT_ALLOWED, "Method not allowed")


@require_http_methods(["GET"])
def find_user(request):
    logger = Logger("find_user")
    if request.method == "GET":
        response = []
        query_params = request.GET.get("q", "")
        query_params = query_params
        list_user = User.filter_user(User, query_params)
        for user in list_user:
            user_to_add = {"id": user.id, "username": user.username}
            response.append(user_to_add)

        logger.log().info("Successfully search user")
        return response_success("Successfully search user", response)

    logger.log().error("Method not allowed")
    return response_error(HTTPStatus.METHOD_NOT_ALLOWED, "Method not allowed")


@require_http_methods(["GET"])
def heroes(request, *args, **kwargs):
    logger = Logger("heroes")
    if request.method == "GET":
        try:
            response = []
            champion_data = requests.get(URL)
            champion_data = champion_data.json()
            champion_list = champion_data["data"]
            query_params = request.GET.get("q", "")
            query_params = query_params.lower()

            if query_params in cache:
                response_data = cache.get(query_params)
                logger.log().info("Successfuly GET from Cache")
                return response_success("Successfully get heroes data", response_data)

            if not query_params:
                for hero, values in champion_list.items():
                    response.append(values)
                logger.log().info("Successfully GET all heroes data")
                cache.set("", response, timeout=CACHE_TTL)
                return response_success("Successfully get heroes data", response)

            for hero, values in champion_list.items():
                if query_params in hero.lower():
                    response.append(values)

            logger.log().info("Successfully GET heroes data")
            cache.set(query_params, response, timeout=CACHE_TTL)
            return response_success("Successfully get heroes data", response)

        except Exception as e:
            logger.log().error(str(e))
            return response_error(
                HTTPStatus.INTERNAL_SERVER_ERROR, "Error when fetching data"
            )

    logger.log().error("Method not allowed")
    return response_error(HTTPStatus.METHOD_NOT_ALLOWED, "Method not allowed")
