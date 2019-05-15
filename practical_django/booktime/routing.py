from channels.routing import ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler
from django.urls import re_path
from .auth import TokenGetAuthMiddlewareStack
import main.routing


application = ProtocolTypeRouter({})
