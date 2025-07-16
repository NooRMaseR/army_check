from django.urls import path
from core.consumers import RequestConsumer

urlpatterns = (
    path("ws/", RequestConsumer.as_asgi()),
)