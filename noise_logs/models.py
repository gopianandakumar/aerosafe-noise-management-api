from django.conf import settings
from django.db import models

from airports.models import Airport
from assets.models import Asset


class NoiseLog(models.Model):

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        RESOLVED = "RESOLVED", "Resolved"

    airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="noise_logs",
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="noise_logs",
    )

    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reported_noise_logs",
    )

    noise_level = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    location = models.CharField(max_length=255)

    description = models.TextField()

    recorded_at = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-recorded_at"]
        indexes = [
            models.Index(fields=["airport", "status"]),
            models.Index(fields=["recorded_at"]),
        ]

    def __str__(self):
        return f"Noise Log #{self.id}"