from .redis import redisInstance
from django.views.decorators.http import require_http_methods


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
def get_heroes(request):
    pass
