from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'role', 'plan')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        role = attrs.get('role')
        plan = attrs.get('plan')

        if role == 'reader' and not plan:
            raise serializers.ValidationError({
                'plan': 'Este campo é obrigatório quando a role é "reader".'
            })
        return attrs

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)