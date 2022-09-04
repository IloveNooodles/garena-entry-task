import json
import logging
import os
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)

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
        try:
            file_name = os.path.join(settings.BASE_DIR, "data", "champion.json")
            print(file_name)
            print(settings.BASE_DIR)
            with open(file_name, "r") as file_champion:
                list_champions = json.load(file_champion)
                selected_champion = list_champions["data"]["Aatrox"]
                response = {
                  "Success": True,
                  "Data": selected_champion,
                }
                return JsonResponse(response)
        except:
            logger.error("Failed to open file")
            return JsonResponse({"ERROR": True})