from django.db import models

from django.contrib.auth.models import User


class ArtistApplication(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applications"
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    genre = models.CharField(max_length=255)
    biography = models.TextField()
    sample_songs = models.FileField(upload_to="sample_songs/")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.status}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_artist = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    genres = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Dispute(models.Model):
    STATUS_CHOICES = (
        ("open", "Open"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    )

    raised_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="disputes_raised"
    )
    against = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="disputes_against"
    )
    description = models.TextField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="open")
    resolution = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispute by {self.raised_by.username} against {self.against.username} - {self.status}"


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ("payment", "Payment"),
        ("refund", "Refund"),
    )

    artist = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer_transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    status = models.CharField(max_length=10, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} - {self.amount} by {self.customer.username} to {self.artist.username}"
