from django.urls import re_path
from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r'^messenger/chat_room/(?P<chatroom_id>[\d]+)/$', consumers.ChatConsumer()),
]