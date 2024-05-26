import uuid as uuid_lib

from django.db import models, transaction
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils.crypto import get_random_string


from core.models import TimestampedModel, storage_location


class UserManager(BaseUserManager):

    use_in_migration = True

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff = True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser = True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_artist = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ["email", "username"]

    def __str__(self):
        return self.username


class UserProfile(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    gender = models.CharField(max_length=100, default="")
    bio = models.TextField(blank=True)
    profile_picture = models.FileField(
        storage=storage_location,
        upload_to="user_profile_picture/",
        null=True,
        blank=True,
    )
    phone_number = models.CharField(max_length=20, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.username


# Admin invitation model
class AdminInvitation(TimestampedModel):
    email = models.EmailField()
    code = models.CharField(max_length=20, unique=True, blank=True)
    inviter = models.ForeignKey(
        User, related_name="sent_invitations", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(20)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invitation for {self.email} by {self.inviter.username} (Accepted: {'Yes' if self.accepted else 'No'})"


# Genre model
class Genre(TimestampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Artist data model
class ArtistData(TimestampedModel):
    genres = models.CharField(max_length=256)


# Artist profile model
class ArtistProfile(UserProfile):
    genres = models.ManyToManyField(Genre, related_name="artist_profile")
    samples = models.FileField(
        storage=storage_location, upload_to="samples/", null=True, blank=True
    )
    price_per_service = models.DecimalField(max_digits=10, decimal_places=2)
    stage_name = models.CharField(max_length=100, default="")

    class Meta:
        verbose_name = "Artist Profile"
        verbose_name_plural = "Artist Profiles"

    def __str__(self):
        return self.user.username


# Customer profile model
class CustomerProfile(UserProfile):
    favorite_genres = models.ManyToManyField(Genre, related_name="customer_profile")

    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"

    def __str__(self):
        return self.user.username


# Admin profile model
class AdminProfile(UserProfile):
    admin_notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Admin Profile"
        verbose_name_plural = "Admin Profiles"

    def __str__(self):
        return self.user.username


# class Message(TimestampedModel):
#     sender = models.ForeignKey(
#         UserProfile, on_delete=models.CASCADE, related_name="sent_messages"
#     )
#     receiver = models.ForeignKey(
#         UserProfile, on_delete=models.CASCADE, related_name="received_messages"
#     )
#     image = models.FileField(
#         storage=storage_location, upload_to="message_images/", null=True, blank=True
#     )
#     message = models.TextField()
#     sent_at = models.DateTimeField(auto_now_add=True)
#     read = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Message from {self.sender} to {self.receiver}"
