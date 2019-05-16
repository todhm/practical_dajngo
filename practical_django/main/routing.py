from channels.auth import AuthMiddlewareStack
from django.urls import path
from booktime.auth import TokenGetAuthMiddlewareStack

from . import consumers

websocket_urlpatterns = [
    path(
        "ws/customer-service/<int:order_id>/",
        consumers.ChatConsumer,
    )
]
