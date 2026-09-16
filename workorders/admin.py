from django.contrib import admin

from .models import WorkOrder


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "inspection",
        "assigned_to",
        "status",
        "due_date",
    )

    search_fields = (
        "title",
        "description",
    )

    list_filter = (
        "status",
        "due_date",
    )