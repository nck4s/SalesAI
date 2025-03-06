from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .consumers import ChatConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/chat/global/", ChatConsumer.as_asgi()),
        ])
    ),
})

websocket_urlpatterns = [
    path("ws/chat/global/", ChatConsumer.as_asgi()),
]