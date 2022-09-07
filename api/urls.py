from django.urls import path
from .views import heroes, register, find_user, login, edit_profile, input_ref

urlpatterns = [
    path("heroes", heroes, name="heroes"),
    path("register", register, name="register"),
    path("users", find_user, name="users"),
    path("login", login, name="login"),
    path("edit_profile", edit_profile, name="edit_profile"),
    path("input_ref", input_ref, name="input_ref"),
]
