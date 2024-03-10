from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "is_admin"]

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
