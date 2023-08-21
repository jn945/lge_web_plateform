from apps.accounts.models import User
from rest_framework import serializers
from reversion.models import Version

from .models import Document, HWCheck, HWCheckInfo, HWCheckRow


class CommonUserField(serializers.RelatedField):
    def to_representation(self, value):
        return {"id": value.id, "name": value.username}

    # def to_internal_value(self, data):
    #     print(data["id"])
    #     return data["id"]

    def to_internal_value(self, data):
        return data["id"]


class HWCheckSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = HWCheck
        fields = "__all__"


class HWCheckRowSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    common_user = CommonUserField(queryset=User.objects.all(), many=True)

    class Meta:
        model = HWCheckRow
        fields = "__all__"


class HWCheckInfoSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = HWCheckInfo
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Document
        fields = "__all__"


class VersionSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Version
        fields = "__all__"
