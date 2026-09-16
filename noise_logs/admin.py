from django.contrib import admin

from .models import NoiseLog


@admin.register(NoiseLog)
class NoiseLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "airport",
        "asset",
        "noise_level",
        "status",
        "recorded_at",
        "reported_by",
    )

    search_fields = (
        "description",
        "location",
    )

    list_filter = (
        "status",
        "airport",
    )