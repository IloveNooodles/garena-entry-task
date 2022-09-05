from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from entry_task.logger import Logger
from http import HTTPStatus
import json
import requests

URL = "https://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json"
TIMEOUT = 3600  # in second
CACHE_TTL = getattr(settings, 'CACHE_TTL', TIMEOUT)


@require_http_methods(["POST"])
def register(request):
    pass


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
    if request.method == "GET":
        logger = Logger("heroes")
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
                {"Status": "Error", "Data": []}, status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
