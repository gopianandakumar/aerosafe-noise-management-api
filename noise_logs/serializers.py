from rest_framework import serializers

from airports.models import Airport
from assets.models import Asset
from .models import NoiseLog


class AirportSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ["id", "name", "code"]


class AssetSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["id", "name", "asset_type", "serial_number"]


class UserSummarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


class NoiseLogSerializer(serializers.ModelSerializer):
    airport_details = AirportSummarySerializer(
        source="airport",
        read_only=True,
    )

    asset_details = AssetSummarySerializer(
        source="asset",
        read_only=True,
    )

    reported_by_details = UserSummarySerializer(
        source="reported_by",
        read_only=True,
    )


    class Meta:
        model = NoiseLog

        fields = [
            "id",

            "airport",
            "airport_details",

            "asset",
            "asset_details",

            "reported_by",
            "reported_by_details",

            "noise_level",
            "location",
            "description",
            "recorded_at",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "reported_by",
            "reported_by_details",
            "airport_details",
            "asset_details",
            "created_at",
            "updated_at",
        ]

    def validate_noise_level(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Noise level cannot be negative."
            )

        if value > 200:
            raise serializers.ValidationError(
                "Noise level cannot exceed 200 dB."
            )

        return value

    def validate(self, attrs):
        status = attrs.get("status")
        description = attrs.get("description")
        noise_level = attrs.get("noise_level")

        if status == "RESOLVED" and not description:
            raise serializers.ValidationError(
                {
                    "description": "Description is required when resolving a noise log."
                }
            )

        if noise_level is not None and noise_level > 80 and status == "RESOLVED":
            raise serializers.ValidationError(
                {
                    "status": "Noise logs above 80 dB must be reviewed before resolution."
                }
            )

        return attrs