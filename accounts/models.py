from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils.crypto import get_random_string


from core.models import TimestampedModel, storage_location


User = settings.AUTH_USER_MODEL


class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is Required")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

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

    objects = UserManager()

    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ["email", "username"]

    def __str__(self):
        return self.username


class UserProfile(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")

    # Additional fields
    is_artist = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    profile_picture = models.FileField(
        storage=storage_location,
        upload_to="user_profile_picture/",
        null=True,
        blank=True,
    )
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


class AdminInvitation(models.Model):
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


class Genre(TimestampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ArtistProfile(TimestampedModel):
    profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="artist_profile"
    )
    genres = models.ManyToManyField(Genre, related_name="artists")
    samples = models.FileField(
        storage=storage_location, upload_to="samples/", null=True, blank=True
    )
    price_per_service = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.profile.user.username


class Message(TimestampedModel):
    sender = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="received_messages"
    )
    image = models.FileField(
        storage=storage_location, upload_to="message_images/", null=True, blank=True
    )
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
