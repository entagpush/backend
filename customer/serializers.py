from rest_framework import serializers

from accounts.models import CustomerProfile
from .models import ArtistReview, Gig, Message


class GigCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
        ]


class GigSerializer(serializers.ModelSerializer):
    customer = GigCustomerSerializer(read_only=True)

    class Meta:
        model = Gig
        fields = [
            "id",
            "customer",
            "artist",
            "description",
            "date",
            "price",
            "status",
        ]
        read_only_fields = ["customer", "status"]

    # def create(self, validated_data):
    #     request = self.context.get("request", None)
    #     if request:
    #         validated_data["customer"] = request.user
    #     return super().create(validated_data)


class ArtistReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistReview
        fields = [
            "id",
            "artist",
            "customer",
            "rating",
            "review",
            "created_at",
        ]
        read_only_fields = ["customer"]

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request:
            validated_data["customer"] = request.user
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "content", "timestamp", "is_read"]
        read_only_fields = ["sender", "timestamp", "is_read"]

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request:
            validated_data["sender"] = request.user
        return super().create(validated_data)
