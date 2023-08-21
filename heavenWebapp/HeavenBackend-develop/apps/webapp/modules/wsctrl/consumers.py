import datetime
import json
import logging
import os
from typing import Any

from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from .data_struct.WsDataStruct import DataTypeEnum, WsDataStruct

WEBSOCKET_LOG_PATH = getattr(settings, "WEBSOCKET_LOG_PATH", None)

os.makedirs(WEBSOCKET_LOG_PATH, exist_ok=True)

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler(
    os.path.join(
        WEBSOCKET_LOG_PATH,
        datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_websocket.log",
    )
)
logger.handlers.append(file_handler)


class WsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name: str = self.scope["url_route"]["kwargs"]["group_name"]
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        logger.info(f"connected : {self.group_name}")

    async def disconnect(self, close_code: Any):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        logger.info(f"disconnected : {self.group_name}")

    async def receive(self, text_data: str):
        try:
            logger.info(f"Message Recieved : {text_data}")
            recieved_data: WsDataStruct = WsDataStruct.from_json(text_data)
        except Exception:
            pass

    async def webapp_message(self, event):
        message = event["message"]
        logger.info(
            "=" * 20
            + f"\nSend Message\nTo : {self.group_name}\nMessage : {message}\n"
            + "=" * 20
        )

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
