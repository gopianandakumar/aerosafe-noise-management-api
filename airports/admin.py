from django.contrib import admin

from .models import Airport


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "location",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "location",
    )

    list_filter = (
        "is_active",
    )