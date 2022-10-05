from django.urls import re_path

from IE.GreenerLife.base import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.VideoConsumer.as_asgi()),
]

