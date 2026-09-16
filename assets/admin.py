from django.contrib import admin

from .models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "asset_type",
        "serial_number",
        "airport",
        "status",
    )

    search_fields = (
        "name",
        "serial_number",
        "asset_type",
    )

    list_filter = (
        "status",
        "asset_type",
        "airport",
    )