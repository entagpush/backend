import uuid as uuid_lib

from django.db import models, transaction
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils.crypto import get_random_string

from cloudinary.models import CloudinaryField

from core.models import TimestampedModel


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
    profile_picture = CloudinaryField(
        "image", null=True, blank=True
    )  # Updated to use Cloudinary
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
    samples = CloudinaryField(
        "file", null=True, blank=True
    )  # Updated to use Cloudinary

    price_per_service = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, null=True
    )

    skilled_profession = models.CharField(max_length=256, default="")
    stage_name = models.CharField(max_length=100, default="")
    ranking = models.FloatField(default=0.0)
    total_rating = models.IntegerField(default=0)  # Sum of all ratings
    number_of_ratings = models.IntegerField(default=0)  # Number of ratings received

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Artist Profile"
        verbose_name_plural = "Artist Profiles"

    def update_ranking(self, new_rating):
        self.total_rating += new_rating
        self.number_of_ratings += 1
        self.ranking = self.total_rating / self.number_of_ratings
        self.save()


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


class VerificationStatusChoices(models.TextChoices):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class UserVerificationRequest(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bvn = models.CharField(max_length=12, default="")
    nin = models.CharField(max_length=12, default="")
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    phone_number = models.CharField(max_length=20, default="")
    date_of_birth = models.DateField(null=True)
    status = models.CharField(
        max_length=20,
        choices=VerificationStatusChoices.choices,
        default="pending",
    )

    def __str__(self):
        return self.user.username

    # document_img = models image field here.


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
