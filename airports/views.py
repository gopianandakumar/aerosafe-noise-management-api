from rest_framework.viewsets import ModelViewSet

from .models import Airport
from .serializers import AirportSerializer


class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer