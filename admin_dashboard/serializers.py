from rest_framework import serializers

from accounts.models import Genre
from customer.models import ArtistApplication


class ArtistApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistApplication
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "genre",
            "biography",
            "sample_songs",
            "status",
            "feedback",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["status", "feedback", "created_at", "updated_at"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"
