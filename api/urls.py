from django.urls import path
from .views import heroes

urlpatterns = [path("heroes", heroes, name="index")]
