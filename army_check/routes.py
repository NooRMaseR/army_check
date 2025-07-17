from django.urls import path
from core.consumers import ActionConsumer, RequestConsumer

urlpatterns = (
    path("ws/", RequestConsumer.as_asgi()),
    path("ws/manager/", ActionConsumer.as_asgi()),
)