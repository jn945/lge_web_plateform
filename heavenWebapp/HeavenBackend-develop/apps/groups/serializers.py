from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import CustomGroup


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomGroup
        fields = "__all__"
