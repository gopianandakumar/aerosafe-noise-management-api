from django.db import models
from airports.models import Airport


class Asset(models.Model):

    class AssetStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        MAINTENANCE = "MAINTENANCE", "Maintenance"

    airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="assets",
    )

    name = models.CharField(max_length=200)
    asset_type = models.CharField(max_length=100)
    serial_number = models.CharField(
        max_length=100,
        unique=True,
    )

    location = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=AssetStatus.choices,
        default=AssetStatus.ACTIVE,
    )

    installation_date = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["airport", "status"]),
            models.Index(fields=["asset_type"]),
        ]

    def __str__(self):
        return self.name