from rest_framework import serializers

from ..CommonCode.models import CommonCode


class CommonCodeSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CommonCode
        fields = "__all__"
