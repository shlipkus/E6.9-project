from django.urls import re_path
from .consumers import PrivetChatConsumer, PublicChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/private/(?P<room_name>[-\w]+)/$", PrivetChatConsumer.as_asgi()),
    re_path(r"ws/rooms/(?P<room_name>[-\w]+)/$", PublicChatConsumer.as_asgi()),
]