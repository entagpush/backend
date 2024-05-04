from django.utils import timezone
from django.contrib.auth import authenticate

from rest_framework import serializers

from accounts.models import User, AdminInvitation, UserProfile
from accounts.services import send_admin_invitation_email


INVALID_CREDENTIALS_MSG = "Unable to login with the provided credentials."


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "is_admin"]

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "is_admin", "date_joined", "is_staff"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "bio",
            "phone_number",
            "is_artist",
            "profile_picture",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = UserDetailsSerializer(instance.user).data
        return representation


class UserDetailsTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = UserProfileSerializer()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def authenticate_user(self, request, **data):
        credentials = {
            "username": data.get("username"),
            "password": data.get("password"),
        }

        user = authenticate(request, **credentials)
        if not user:
            raise serializers.ValidationError(
                {
                    "detail": INVALID_CREDENTIALS_MSG,
                }
            )
        return user

    def save(self):
        request = self.context.get("request")
        user = self.authenticate_user(request, **self.validated_data)

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])
        return user


class AdminInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminInvitation
        fields = ["id", "email", "inviter", "code"]
        read_only_fields = (
            "code",
            "inviter",
        )

    def create(self, validated_data):
        invitation = AdminInvitation.objects.create(**validated_data)
        # Send email to the invitee with the invitation code/link
        send_admin_invitation_email(invitation)
        return invitation
