import json
import os
from entry_task.logger import Logger
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings


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
def get_heroes(request, *args, **kwargs):
    if request.method == "GET":
        logger = Logger("get_heroes")
        try:
            file_name = os.path.join(settings.BASE_DIR, "data", "champion.json")
            with open(file_name, "r") as file_champion:
                list_champions = json.load(file_champion)
                selected_champion = list_champions["data"]["Aatrox"]
                response = {
                  "Success": True,
                  "Data": selected_champion,
                }
                logger.log().info("Successfuly get champions data")
                return JsonResponse(response)
        except:
            logger.log().error("Failed to open file")
            return JsonResponse({"ERROR": True})