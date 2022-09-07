from django.core.validators import validate_email as v
from django.core.exceptions import ValidationError
from django.http import JsonResponse


def validate_email(email):
    try:
        v(email)
        return True
    except ValidationError:
        return False


def response_error(status, message):
    return JsonResponse(
        {"Status": "Error", "Data": [], "Message": message}, status=status
    )
