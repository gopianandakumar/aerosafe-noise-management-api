from rest_framework.viewsets import ModelViewSet

from .models import Inspection
from .serializers import InspectionSerializer


class InspectionViewSet(ModelViewSet):
    queryset = (
        Inspection.objects
        .select_related("noise_log", "inspected_by")
    )

    serializer_class = InspectionSerializer

    filterset_fields = [
        "noise_log",
        "status",
        "inspection_type",
    ]

    search_fields = [
        "findings",
        "inspection_type",
    ]

    ordering_fields = [
        "created_at",
        "inspected_at",
    ]

    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(inspected_by=self.request.user)