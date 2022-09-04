from django.urls import path
from .views import get_heroes

urlpatterns = [
    path("", get_heroes, name="index")
]
