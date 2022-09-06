from django.urls import path
from .views import heroes, register, find_user, login

urlpatterns = [
    path("heroes", heroes, name="heroes"),
    path("register", register, name="register"),
    path("users", find_user, name="users"),
    path("login", login, name="login")
]
