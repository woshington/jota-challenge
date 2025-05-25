from core.models import Vertical, Plan
from rest_framework import serializers


class VerticalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vertical
        exclude = ["created_at", "updated_at"]


class PlanSerializer(serializers.ModelSerializer):
    vertical = VerticalSerializer(many=True)
    class Meta:
        model = Plan
        exclude = ["created_at", "updated_at"]