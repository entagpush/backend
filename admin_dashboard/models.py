from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


from core.models import TimestampedModel, storage_location

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
    proof = models.FileField(
        storage=storage_location, upload_to="proof/", null=True, blank=True
    )

    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispute by {self.raised_by.username} against {self.against.username} - {self.status}"


# class TimestampedModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(
#         User,
#         null=True,
#         blank=True,
#         related_name="%(class)s_created",
#         on_delete=models.SET_NULL,
#     )
#     updated_by = models.ForeignKey(
#         User,
#         null=True,
#         blank=True,
#         related_name="%(class)s_updated",
#         on_delete=models.SET_NULL,
#     )

#     class Meta:
#         abstract = True
