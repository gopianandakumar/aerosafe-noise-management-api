from rest_framework import serializers

from .models import Inspection


class InspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspection
        fields = [
            "id",
            "noise_log",
            "inspection_type",
            "findings",
            "status",
            "inspected_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]