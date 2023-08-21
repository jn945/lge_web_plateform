from rest_framework import serializers

from .models import Plan, PlanGroup, PlanGroupInfo, PlanInfo, PlanSeries


class PlanInfoSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PlanInfo
        fields = "__all__"


class PlanSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Plan
        fields = "__all__"


class PlanSeriesSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PlanSeries
        fields = "__all__"


class PlanGroupInfoSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PlanGroupInfo
        fields = "__all__"


class PlanGroupSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PlanGroup
        fields = (
            "id",
            "created_at",
            "creator",
            "plan",
            "plan_type",
            "group_name",
            "details",
        )
