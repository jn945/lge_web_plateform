from django.urls import path

from .modules.wsctrl import consumers
from .views import (
    WebAppCmdPause,
    WebAppCmdResume,
    WebAppCmdStart,
    WebAppCmdStop,
    WebSocketSend,
)

websocket_urlpatterns = [
    path("webapp/<str:group_name>/", consumers.WsConsumer.as_asgi()),
]

urlpatterns = [
    path("api/v1/webapp/send", WebSocketSend.as_view()),
    path("api/v1/webapp/cmd-start", WebAppCmdStart.as_view()),
    path("api/v1/webapp/cmd-stop", WebAppCmdStop.as_view()),
    path("api/v1/webapp/cmd-pause", WebAppCmdPause.as_view()),
    path("api/v1/webapp/cmd-resume", WebAppCmdResume.as_view()),
]
