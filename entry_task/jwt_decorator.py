from functools import wraps
from entry_task.jwt_auth import JWTAuth


# def auth(func):
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):
#       try:
#         return func(request, *args, **kwargs)
#       except:

#     return wrapper