from channels.routing import ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler
from django.urls import re_path
from .auth import TokenGetAuthMiddlewareStack
from channels.auth import AuthMiddlewareStack
import main.routing
from main import consumers


application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": TokenGetAuthMiddlewareStack(
            URLRouter(main.routing.websocket_urlpatterns)
        ),
        "http": URLRouter(
            main.routing.http_urlpatterns
            + [re_path(r"", AsgiHandler)]
        )
    }
)
