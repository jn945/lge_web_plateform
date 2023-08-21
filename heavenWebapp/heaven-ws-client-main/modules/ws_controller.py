import logging

import websockets
from modules.data_struct.WsDataStruct import DataTypeEnum, WsDataStruct
from modules.tester_controller import excute_cmd

logger = logging.getLogger(__name__)


class WebSocketController:
    def __init__(self, url, callback=logger.info):
        self.callback = callback
        self.url = url

    async def on_message(self, msg):
        self.callback(f"received message : {msg}")
        ws_data = WsDataStruct.from_json(msg)
        if ws_data.data_type == DataTypeEnum.COMMAND.value:
            await excute_cmd(self._ws, ws_data)

    def on_error(self, msg):
        self.callback(msg)

    def on_close(self, close_msg):
        self._ws.disconnet()
        self.callback("closed")

    async def connect(self):
        # 웹 소켓에 접속을 합니다.
        async with websockets.connect(self.url) as ws:
            logger.info(f"connetcted : {self.url}")
            self._ws = ws

            while True:
                try:
                    data = await self._ws.recv()
                    await self.on_message(data)
                except websockets.exceptions.ConnectionClosed:
                    logger.error("disconnected")
                    break
