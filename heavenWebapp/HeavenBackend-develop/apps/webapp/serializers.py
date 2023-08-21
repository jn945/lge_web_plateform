from rest_framework import serializers
from rest_framework_dataclasses.serializers import DataclassSerializer

from .modules.wsctrl.data_struct.WsDataStruct import (
    CommandEnum,
    DataTypeEnum,
    WsDataStruct,
)


class WebSocketSendSerializer(serializers.Serializer):
    group_name = serializers.IPAddressField()
    message = serializers.JSONField()

    def get_serialized(self) -> any:
        if self.is_valid():
            return self.validated_data
        else:
            return None


class WebAppCmdStartSerializer(DataclassSerializer):
    class Meta:
        dataclass = WsDataStruct

    def get_serialized(self) -> WsDataStruct:
        self.initial_data["data_type"] = DataTypeEnum.COMMAND.value
        self.initial_data["data"]["cmd"] = CommandEnum.START.value

        if self.is_valid():
            return self.validated_data
        else:
            return None


class WebAppCmdStopSerializer(DataclassSerializer):
    class Meta:
        dataclass = WsDataStruct

    def get_serialized(self) -> WsDataStruct:
        self.initial_data["data_type"] = DataTypeEnum.COMMAND.value
        self.initial_data["data"] = {"cmd": CommandEnum.STOP.value}

        if self.is_valid():
            return self.validated_data
        else:
            return None


class WebAppCmdPauseSerializer(DataclassSerializer):
    class Meta:
        dataclass = WsDataStruct

    def get_serialized(self) -> WsDataStruct:
        self.initial_data["data_type"] = DataTypeEnum.COMMAND.value
        self.initial_data["data"] = {"cmd": CommandEnum.PAUSE.value}

        if self.is_valid():
            return self.validated_data
        else:
            return None


class WebAppCmdResumeSerializer(DataclassSerializer):
    class Meta:
        dataclass = WsDataStruct

    def get_serialized(self) -> WsDataStruct:
        self.initial_data["data_type"] = DataTypeEnum.COMMAND.value
        self.initial_data["data"] = {"cmd": CommandEnum.RESUME.value}

        if self.is_valid():
            return self.validated_data
        else:
            return None
