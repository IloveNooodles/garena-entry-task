from django.urls import path
from .views import heroes, register

urlpatterns = [path("heroes", heroes, name="heroes"),
               path("register", register, name="register")]
