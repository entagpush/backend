from django.utils import timezone
from django.contrib.auth import authenticate
from django.db import transaction

from rest_framework import serializers

from accounts.models import (
    AdminProfile,
    ArtistProfile,
    CustomerProfile,
    User,
    AdminInvitation,
    UserProfile,
)
from accounts.services import send_admin_invitation_email


INVALID_CREDENTIALS_MSG = "Unable to login with the provided credentials."


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "password",
            "is_admin",
            "is_artist",
            "is_customer",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email")
        username_data = validated_data.pop("username")

        if not email:
            raise serializers.ValidationError("The given email must be set")
        if not username_data:
            raise serializers.ValidationError("The given username must be set")

        with transaction.atomic():
            user = User(
                username=User.normalize_username(username_data),
                email=email,
                **validated_data
            )
            user.set_password(password)
            user.save()

            self.create_user_profile(user, validated_data)

        return user

    @staticmethod
    def create_user_profile(user, validated_data):
        if user.is_artist:
            ArtistProfile.objects.create(user=user)
        elif user.is_customer:
            CustomerProfile.objects.create(user=user)
        elif user.is_admin:
            AdminProfile.objects.create(user=user)
        else:
            return serializers.ValidationError(
                detail="Provided user type is invalid", code=400
            )


# class UserDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "email", "username", "is_admin", "date_joined", "is_staff"]


# class UserProfileSerializer(serializers.ModelSerializer):
#     user = UserDetailsSerializer(read_only=True)

#     class Meta:
#         model = UserProfile
#         fields = [
#             "id",
#             "user",
#             "first_name",
#             "last_name",
#             "bio",
#             "phone_number",
#             "is_artist",
#             "profile_picture",
#         ]

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         return representation


# class UserProfileCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = [
#             "user",
#             "first_name",
#             "last_name",
#             "bio",
#             "phone_number",
#             "is_artist",
#         ]

#         read_only_fields = ("user",)

#     def to_representation(self, instance):
#         return UserProfileSerializer(instance=instance)


class ArtistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistProfile
        fields = "__all__"


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = "__all__"


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = "__all__"


class UserDetailsTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    # user = UserProfileSerializer()


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
