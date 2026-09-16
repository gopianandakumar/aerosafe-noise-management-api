from django.db import models

from django.conf import settings
from noise_logs.models import NoiseLog


class Inspection(models.Model):

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"

    noise_log = models.ForeignKey(
        NoiseLog,
        on_delete=models.CASCADE,
        related_name="inspections",
    )

    inspection_type = models.CharField(
        max_length=100,
    )

    findings = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )

    inspected_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    inspected_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    related_name="inspections",
    null=True,
    blank=True
)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Inspection #{self.id}"