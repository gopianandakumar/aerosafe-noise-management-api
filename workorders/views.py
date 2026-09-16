from rest_framework.viewsets import ModelViewSet

from .models import WorkOrder
from .serializers import WorkOrderSerializer


class WorkOrderViewSet(ModelViewSet):
    queryset = (
        WorkOrder.objects
        .select_related(
            "inspection",
            "assigned_to",
        )
    )

    serializer_class = WorkOrderSerializer

    filterset_fields = [
        "inspection",
        "assigned_to",
        "status",
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "due_date",
    ]

    ordering = ["-created_at"]