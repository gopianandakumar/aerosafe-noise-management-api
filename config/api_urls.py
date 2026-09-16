from rest_framework.routers import DefaultRouter

from airports.views import AirportViewSet
from assets.views import AssetViewSet
from noise_logs.views import NoiseLogViewSet
from inspections.views import InspectionViewSet
from workorders.views import WorkOrderViewSet


router = DefaultRouter()

router.register(
    "airports",
    AirportViewSet,
    basename="airport",
)

router.register(
    "assets",
    AssetViewSet,
    basename="asset",
)

router.register(
    "noise-logs",
    NoiseLogViewSet,
    basename="noise-log",
)

router.register(
    "inspections",
    InspectionViewSet,
    basename="inspection",
)

router.register(
    "work-orders",
    WorkOrderViewSet,
    basename="work-order",
)

urlpatterns = router.urls