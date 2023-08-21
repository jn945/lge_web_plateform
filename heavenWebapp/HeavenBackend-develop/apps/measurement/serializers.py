from django.contrib.auth.models import Group
from rest_framework import serializers

from modules.common.utils import remove_creator

from .models import MeasurementRequest, Result, TestItemInfo


class TestItemInfoSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TestItemInfo
        fields = "__all__"


class MeasurementRequestSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MeasurementRequest
        fields = "__all__"


class ResultSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Result
        fields = "__all__"
