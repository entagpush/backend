from django.db import models
from django.conf import settings

from cloudinary.models import CloudinaryField

from core.models import TimestampedModel

"""
to access history records ===
instance = MyModel.objects.get(id=1)
for history in instance.history.all():
    print(history.history_date, history.history_user_id)

"""

User = settings.AUTH_USER_MODEL


class Dispute(TimestampedModel):
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
    proof = CloudinaryField("file", null=True, blank=True)

    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispute by {self.raised_by.username} against {self.against.username} - {self.status}"
