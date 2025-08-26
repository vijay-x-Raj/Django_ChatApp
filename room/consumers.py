import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # room_name taken from URL (<str:room_name>) – we treat it as the room slug
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope.get('user')

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):  # close_code retained for completeness
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Parse JSON safely
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        message = (data.get('message') or '').strip()

        # Only proceed for authenticated users & non‑empty messages
        if not message or not (self.user and self.user.is_authenticated):
            return

        # Persist message (ignore if room slug invalid)
        await self.save_message(self.user, self.room_name, message)

        # Broadcast to everyone in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
            }
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    'message': event['message'],
                    'username': event['username'],
                }
            )
        )

    @sync_to_async
    def save_message(self, user, room_slug, content):
        try:
            room = Room.objects.get(slug=room_slug)
        except Room.DoesNotExist:
            return  # Silently ignore if slug invalid (prevents socket crash)
        Message.objects.create(user=user, room=room, content=content)