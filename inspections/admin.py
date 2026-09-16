from django.contrib import admin

from .models import Inspection


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "noise_log",
        "inspection_type",
        "status",
        "inspected_at",
    )

    search_fields = (
        "inspection_type",
        "findings",
    )

    list_filter = (
        "status",
    )