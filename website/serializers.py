from rest_framework import serializers
from website.models import Blog, Waitlist


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title", "content", "created_at", "updated_at"]


class WaitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = ["id", "name", "email", "phone_number", "is_artist"]
