from rest_framework import serializers

from website.models import Blog, Waitlist


class BlogSerializer(serializers.ModelSerializer):
    model = Blog
    fields = "__all__"


class WaitListSerializer(serializers.ModelSerializer):
    model = Waitlist
    fields = "__all__"
