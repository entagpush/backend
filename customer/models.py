from django.core.mail import send_mail
from django.db import models
from django.conf import settings

from cloudinary.models import CloudinaryField
from storages.backends.s3boto3 import S3Boto3Storage

from accounts.models import ArtistProfile
from core.models import TimestampedModel

User = settings.AUTH_USER_MODEL


class ArtistApplication(TimestampedModel):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    genre = models.CharField(max_length=255)
    biography = models.TextField()

    sample_songs = CloudinaryField(
        "file", null=True, blank=True
    )  # Updated to use Cloudinary

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    feedback = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.status}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == "pending":
            self.notify_admin()

    def notify_admin(self):
        send_mail(
            "New Artist Application Submitted",
            f"Artist {self.name} has submitted an application.",
            "from@example.com",
            ["admin@example.com"],
            fail_silently=False,
        )


class Gig(TimestampedModel):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("counter_offer", "Counter Offer"),
        ("completed", "Completed"),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gigs")
    artist = models.ForeignKey(
        ArtistProfile, on_delete=models.CASCADE, related_name="gigs"
    )
    description = models.TextField()
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    reason_for_rejection = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Gig for {self.artist.user.username} by {self.customer.username} on {self.date}"


class ArtistReview(TimestampedModel):
    artist = models.ForeignKey(
        ArtistProfile, on_delete=models.CASCADE, related_name="reviews"
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()  # e.g., 1 to 5 stars
    review = models.TextField(blank=True)

    def __str__(self):
        return f"Review for {self.artist.user.username} by {self.customer.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.artist.update_ranking(self.rating)


class Message(TimestampedModel):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_counter_offer = models.BooleanField(default=False)
    gig = models.ForeignKey(
        Gig, on_delete=models.CASCADE, related_name="gig_messages", null=True
    )

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


# from customer.signals import application_notification
