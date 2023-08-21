from apps.accounts.models import User
from rest_framework import serializers
from reversion.models import Version

from ..virtualanalysis.models import CAEData, VirtualAnalysisRequest


class CommonUserField(serializers.RelatedField):
    def to_representation(self, value):
        return {"id": value.id, "name": value.username}

    # def to_internal_value(self, data):
    #     print(data["id"])
    #     return data["id"]

    def to_internal_value(self, data):
        return data["id"]


class VirtualAnalysisRequestSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = VirtualAnalysisRequest
        fields = "__all__"


class CAEDataSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CAEData
        fields = "__all__"
