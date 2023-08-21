from rest_framework import serializers

from .models import Power, PowerInfo, Soc, SocInfo


class SocSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Soc
        fields = "__all__"


class SocInfoSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SocInfo
        fields = "__all__"


class PowerSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Power
        fields = "__all__"


class PowerInfoSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PowerInfo
        fields = "__all__"
