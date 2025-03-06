import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "global"
        self.room_group_name = f"chat_{self.room_name}"
        
        logger.info("✅ WebSocket подключён")
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logger.warning(f"🔴 WebSocket отключён: {close_code}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        logger.info(f"📩 Получено сообщение: {text_data}")

        data = json.loads(text_data)
        user = "User"  # В будущем можно менять на реального пользователя
        message = data["message"]

        # Сохраняем сообщение в базе данных
        chat_message = ChatMessage.objects.create(user=user, message=message)

        # Отправляем сообщение в WebSocket
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": chat_message.message}
        )

    async def chat_message(self, event):
        logger.info(f"📤 Отправка сообщения: {event['message']}")
        await self.send(text_data=json.dumps({"message": event["message"]}))
