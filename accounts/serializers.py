from rest_framework import serializers

from accounts.models import User, AdminInvitation
from accounts.services import send_admin_invitation_email


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "is_admin"]

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
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
