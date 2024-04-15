from rest_framework.exceptions import PermissionDenied
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
            "updated_at",
        ]
        extra_kwargs = {"author": {"read_only": True, "required": False}}

    def create(self, validated_data):
        request = self.context.get('request')
        print(request, request.user)
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if validated_data.get("is_anonymous") != True:
                validated_data["author"] = request.user
        else:
            # Optionally raise an exception if an unauthenticated user tries to create a blog without anonymity
            if validated_data.get("is_anonymous") != True:
                raise PermissionDenied("You must be logged in to author a blog post.")

        return super().create(validated_data=validated_data)


class WaitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = ["id", "name", "email", "phone_number", "is_artist"]
