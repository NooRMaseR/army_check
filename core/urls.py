from django.urls import path
from .views import home, manager

urlpatterns = (
    path("", home, name="home"),
    path("manager/", manager, name="manager"),
)
