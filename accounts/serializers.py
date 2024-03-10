from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "is_admin"]

        def create(self, validated_data):
            user = User.objects.create_user(
                email=validated_data["email"], password=validated_data["password"]
            )
            return user
