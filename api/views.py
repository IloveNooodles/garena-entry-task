from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from entry_task.logger import Logger
from entry_task.hash import HashPassword
from http import HTTPStatus
from api.models import User
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

        # check all the field
        if "username" and "password" and "name" and "email" not in request_body:
            return JsonResponse(
                {
                    "Status": "Error",
                    "Data": [],
                    "Message": "Please fill the request body correctly",
                },
                status=HTTPStatus.BAD_REQUEST,
            )

        # find user by ref code
        referred_user = None
        if "ref_code" in request_body:
            referred_user = User.find_user_by_ref(User, request_body["ref_code"])

        if not referred_user and "ref_code" in request_body:
            return JsonResponse(
                {
                    "Status": "Error",
                    "Data": [],
                    "Message": "No user found with inputted referral code",
                },
                status=HTTPStatus.NOT_FOUND,
            )

        # Username validation
        if User.find_user_by_username(User, username=request_body["username"]):
            return JsonResponse(
                {
                    "Status": "Error",
                    "Data": [],
                    "Message": "Username is already exists",
                },
                status=HTTPStatus.CONFLICT,
            )

        # Email validation
        try:
            validate_email(request_body["email"])
        except ValidationError as e:
            logger.log().error(str(e))
            return JsonResponse(
                {
                    "Status": "Error",
                    "Data": [],
                    "Message": "Please provide correct email",
                },
                status=HTTPStatus.UNPROCESSABLE_ENTITY,
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
        response["password"] = hashed_password
        return JsonResponse(
            {
                "Status": "Ok",
                "Data": response,
                "Message": "Successfuly create new user",
            },
            status=HTTPStatus.CREATED,
        )

    logger.log().error("Method not allowed")
    return JsonResponse(
        {"Status": "Error", "Message": "Method not allowed"},
        status=HTTPStatus.METHOD_NOT_ALLOWED,
    )


def login(request):
    pass


def edit_profile(request):
    pass


def input_ref(request):
    pass


def find_user(request):
    pass


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

            if query_params in cache:
                response_data = cache.get(query_params)
                logger.log().info("Successfuly GET from Cache")
                return JsonResponse({"Status": "Ok", "Data": response_data})

            if not query_params:
                for hero, values in champion_list.items():
                    response.append(values)
                logger.log().info("Successfully GET all heroes data")
                cache.set("", response, timeout=CACHE_TTL)
                return JsonResponse({"Status": "Ok", "Data": response})

            for hero, values in champion_list.items():
                if query_params in hero:
                    response.append(values)

            logger.log().info("Successfully GET heroes data")
            cache.set(query_params, response, timeout=CACHE_TTL)
            return JsonResponse({"Status": "Ok", "Data": response})
        except Exception as e:
            logger.log().error(str(e))
            return JsonResponse(
                {"Status": "Error", "Message": "Error when fetching data"},
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
    logger.log().error("Method not allowed")
    return JsonResponse(
        {"Status": "Error", "Message": "Method not allowed"},
        status=HTTPStatus.METHOD_NOT_ALLOWED,
    )
