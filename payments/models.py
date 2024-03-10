from django.db import models
from django.conf import settings


from core.models import TimestampedModel, storage_location

User = settings.AUTH_USER_MODEL


class Transaction(TimestampedModel):
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

    def __str__(self):
        return f"{self.transaction_type.capitalize()} - {self.amount} by {self.customer.username} to {self.artist.username}"
