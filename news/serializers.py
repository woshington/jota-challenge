from django.utils import timezone
from rest_framework import serializers

from core.serializers import VerticalSerializer
from news.models import News


class NewsSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = News
        exclude = ['created_at', 'updated_at']
        read_only_fields = ('id', 'published_at', 'author')

    @staticmethod
    def validate_scheduled_at(value):
        if value:
            now = timezone.now()
            if value < now:
                raise serializers.ValidationError("Scheduled date must be in the future")
            if value.minute != 0 or value.second != 0:
                raise serializers.ValidationError("Scheduled time must be at closed hours (e.g., 13:00, not 13:30)")
        return value

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data["published_at"] = timezone.now() if validated_data.get("status") == News.Status.PUBLISHED else None
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['vertical'] = VerticalSerializer(instance.vertical.all(), many=True).data
        return representation