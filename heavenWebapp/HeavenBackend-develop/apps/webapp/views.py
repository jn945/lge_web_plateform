from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from modules.common.params import webapp_cmd_start_request_schema_dict
from rest_framework import status, views
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    WebAppCmdPauseSerializer,
    WebAppCmdResumeSerializer,
    WebAppCmdStartSerializer,
    WebAppCmdStopSerializer,
    WebSocketSendSerializer,
)


# Create your views here.
def send_message_to_channel_layer(group_name: str, message: dict | str):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name, {"type": "webapp.message", "message": message}
    )


class WebSocketSend(views.APIView):
    @swagger_auto_schema(
        operation_description="websocket message send",
        tags=["[webapp]"],
        request_body=WebSocketSendSerializer,
    )
    @action(detail=False, methods=["post"])
    def post(self, request, format=None):
        serializer = WebSocketSendSerializer(data=request.data)
        request_data = serializer.get_serialized()
        if request_data:
            send_message_to_channel_layer(
                request_data["group_name"], request_data["message"]
            )
            return Response(
                {"message": f"Message sent to {request_data['group_name']}"}
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WebAppCmdStart(views.APIView):
    @swagger_auto_schema(
        operation_description="webapp send cmd-start to client",
        tags=["[webapp]"],
        request_body=webapp_cmd_start_request_schema_dict,
    )
    @action(detail=False, methods=["post"])
    def post(self, request, format=None):
        serializer = WebAppCmdStartSerializer(data=request.data)
        request_data = serializer.get_serialized()

        if request_data:
            send_message_to_channel_layer(request_data.device_ip, request_data.__dict__)
            return Response({"message": f"Message sent to {request_data.device_ip}"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WebAppCmdStop(views.APIView):
    request_schema_dict = openapi.Schema(
        title=("WebAppCmdStop"),
        type=openapi.TYPE_OBJECT,
        properties={
            "device_ip": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=("device_ip"),
                example="127.0.1.1",
            ),
            "test_id": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=("test_id"),
                example="test_1",
            ),
        },
    )

    @swagger_auto_schema(
        operation_description="webapp send cmd-stop to client",
        tags=["[webapp]"],
        request_body=request_schema_dict,
    )
    @action(detail=False, methods=["post"])
    def post(self, request, format=None):
        serializer = WebAppCmdStopSerializer(data=request.data)
        request_data = serializer.get_serialized()

        if request_data:
            send_message_to_channel_layer(request_data.device_ip, request_data.__dict__)
            return Response({"message": f"Message sent to {request_data.device_ip}"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WebAppCmdPause(views.APIView):
    request_schema_dict = openapi.Schema(
        title=("WebAppCmdPause"),
        type=openapi.TYPE_OBJECT,
        properties={
            "device_ip": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=("device_ip"),
                example="127.0.1.1",
            ),
            "test_id": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=("test_id"),
                example="test_1",
            ),
        },
    )

    @swagger_auto_schema(
        operation_description="webapp send cmd-pause to client",
        tags=["[webapp]"],
        request_body=request_schema_dict,
    )
    @action(detail=False, methods=["post"])
    def post(self, request, format=None):
        serializer = WebAppCmdPauseSerializer(data=request.data)
        request_data = serializer.get_serialized()

        if request_data:
            send_message_to_channel_layer(request_data.device_ip, request_data.__dict__)
            return Response({"message": f"Message sent to {request_data.device_ip}"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WebAppCmdResume(views.APIView):
    request_schema_dict = openapi.Schema(
        title=("WebAppCmdPause"),
        type=openapi.TYPE_OBJECT,
        properties={
            "device_ip": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=("device_ip"),
                example="127.0.1.1",
            ),
            "test_id": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=("test_id"),
                example="test_1",
            ),
        },
    )

    @swagger_auto_schema(
        operation_description="webapp send cmd-resume to client",
        tags=["[webapp]"],
        request_body=request_schema_dict,
    )
    @action(detail=False, methods=["post"])
    def post(self, request, format=None):
        serializer = WebAppCmdResumeSerializer(data=request.data)
        request_data = serializer.get_serialized()

        if request_data:
            send_message_to_channel_layer(request_data.device_ip, request_data.__dict__)
            return Response({"message": f"Message sent to {request_data.device_ip}"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
