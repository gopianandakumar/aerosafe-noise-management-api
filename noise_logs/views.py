from rest_framework.viewsets import ModelViewSet

from users.permissions import IsOperationsUser

from .models import NoiseLog
from .serializers import NoiseLogSerializer
from .filters import NoiseLogFilter


class NoiseLogViewSet(ModelViewSet):
    queryset = (
        NoiseLog.objects
        .select_related("airport", "asset", "reported_by")
        .prefetch_related("inspections")
    )

    serializer_class = NoiseLogSerializer

    permission_classes = [IsOperationsUser]

    filterset_class = NoiseLogFilter


    search_fields = [
        "description",
        "location",
    ]

    ordering_fields = [
        "recorded_at",
        "noise_level",
        "created_at",
    ]

    ordering = ["-recorded_at"]

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)