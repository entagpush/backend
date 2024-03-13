from rest_framework import serializers
from website.models import Blog, Waitlist


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title", 
            "content",
            "image",
            "is_anonymous",
            "co_author",
            "author",
            "created_at", 
            "updated_at"
        ]

    def create(self, validated_data):
        if validated_data.get("is_anonymous") != True:
            validated_data["author"] = self.context["request"].user
        return super().create(validated_data=validated_data)



class WaitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = ["id", "name", "email", "phone_number", "is_artist"]
