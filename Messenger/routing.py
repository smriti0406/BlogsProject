from django.urls import re_path
from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r'^chatroom/(?P<chatroom_id>[\d]+)/$', consumers.ChatConsumer),
]