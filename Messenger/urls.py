from django.urls import path
from . import views


app_name = 'Messenger'
urlpatterns = [
    path('', views.index, name='messenger-index'),
    path('chat_room/<int:chatroom_id>', views.chatroom, name='messenger-chatroom'),
    path('NewChat/', views.newchat, name='messenger-newchat')
]