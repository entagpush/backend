from django.db import models
from django.utils import timezone

from cloudinary.models import CloudinaryField

from core.models import TimestampedModel


# Create your models here.


class Blog(TimestampedModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = CloudinaryField("image", null=True, blank=True)  # Updated to use Cloudinary
    is_anonymous = models.BooleanField(default=True)
    co_author = models.CharField(max_length=256, default="", blank=True)
    author = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.author:
            return f"{self.title} created by {self.author}"
        else:
            return f"{self.title} (Anonymous)"


class Waitlist(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)

    is_artist = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
