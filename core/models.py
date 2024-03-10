from django.db import models
from django.conf import settings
from django.utils import timezone

from simple_history.models import HistoricalRecords

from storages.backends.s3boto3 import S3Boto3Storage


storage_location = S3Boto3Storage(location="uploads")


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
