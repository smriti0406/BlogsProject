import asyncio
import json
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, ChatMessage


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })
        chat_room_id = self.scope['url_route']['kwargs']['chatroom_id']
        me = self.scope['user']
        self.chat_room = await self.get_chat_room(chat_room_id)
        self.chat_room_name = f"chat_{self.chat_room}"
        await self.channel_layer.group_add(
            self.chat_room_name,
            self.channel_name
        )
        #print(me, friend)

    async def websocket_receive(self, event):
        print("receive", event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')

            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.username
            myResponse = {
                'message': msg,
                'username': username
            }
            await self.create_chat_message(msg)
            await self.channel_layer.group_send(
                self.chat_room_name,
                {
                    "type": "chat_message",
                    "text": json.dumps(myResponse)
                }
            )

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def get_chat_room(self, chat_room_id):
        chat_room = ChatRoom.objects.get(pk=chat_room_id)
        return chat_room

    @database_sync_to_async
    def get_friend(self, user_id):
        friend = get_object_or_404(User, pk=user_id)
        return friend

    @database_sync_to_async
    def create_chat_message(self, msg):
        me = self.scope['user']
        chat_room = ChatMessage.objects.create(chatroom=self.chat_room, author=me, message=msg)
        return chat_room
