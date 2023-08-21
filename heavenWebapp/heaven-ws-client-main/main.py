import asyncio
import logging
import os

from modules.common.utils.func import get_ip
from modules.config import Config
from modules.ws_controller import WebSocketController

if __name__ == "__main__":
    # config 설정
    config_path = os.path.join("config", "config.ini")
    config = Config.instance(config_path).config

    # logger 설정
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s:%(name)s:%(asctime)s] %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        handlers=[logging.StreamHandler()],
    )
    logger = logging.getLogger(__name__)

    server_url = config["websocket"]["url"] + get_ip() + "/"
    ws = WebSocketController(server_url)

    try:
        asyncio.run(ws.connect())
    except KeyboardInterrupt:
        logger.error("KeyboardInterrupt")
