from functools import wraps
from entry_task.jwt_auth import JWTAuth


def auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      try:
        print("a")
      except:
        print("b")