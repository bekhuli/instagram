import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from chat.models import ChatRoom, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.user_id = self.scope['url_route']['kwargs']['user_id']

        if not self.user.is_authenticated:
            await self.close()
            return

        self.other_user = await database_sync_to_async(User.objects.get)(id=self.user_id)
        self.room, _ = await database_sync_to_async(ChatRoom.objects.get_or_create)(
            user1=min(self.user, self.other_user, key=lambda x: x.id),
            user2=max(self.user, self.other_user, key=lambda x: x.id),
        )

        self.room_group_name = f"chat_{self.room.id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        new_message = await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": new_message,
                "sender": self.user.username,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, message):
        msg = Message.objects.create(room=self.room, sender=self.user, content=message)
        return msg.content