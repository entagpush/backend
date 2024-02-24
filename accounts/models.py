from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # One-to-one link to the Django User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # Additional fields
    is_artist = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", null=True, blank=True
    )
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ArtistProfile(models.Model):
    profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="artist_profile"
    )
    genres = models.ManyToManyField(Genre, related_name="artists")
    samples = models.FileField(
        upload_to="artist_samples/", null=True, blank=True
    )  # Consider a separate model for multiple files
    price_per_service = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.profile.user.username
