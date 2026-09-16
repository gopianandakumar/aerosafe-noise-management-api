import django_filters

from .models import NoiseLog


class NoiseLogFilter(django_filters.FilterSet):
    min_noise_level = django_filters.NumberFilter(
        field_name="noise_level",
        lookup_expr="gte",
    )

    max_noise_level = django_filters.NumberFilter(
        field_name="noise_level",
        lookup_expr="lte",
    )

    class Meta:
        model = NoiseLog
        fields = [
            "airport",
            "asset",
            "status",
            "reported_by",
            "min_noise_level",
            "max_noise_level",
        ]