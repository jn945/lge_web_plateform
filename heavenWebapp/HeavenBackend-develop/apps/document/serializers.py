from rest_framework import serializers
from reversion.models import Version

from .models import ProductSpecification


class ProductSpecificationSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProductSpecification
        fields = "__all__"
