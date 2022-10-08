from django.urls import re_path

from base import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.VideoConsumer.as_asgi()),
]

