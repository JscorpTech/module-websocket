import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if user is None or not user.is_authenticated:
            logging.warning("Muvofaqiyatsiz ulanishga urunish")
            await self.close(4001)
            return
        logging.info("Yangi ulanish")
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logging.info("Websocket uzulish code=%s", close_code)
        await self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        logging.info("Websocket yangi xabar data=%s", text_data)
        await self.channel_layer.group_send(
            "chat", {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
