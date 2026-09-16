from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from llm.serializers import AssetQuestionSerializer
from llm.services import AssetLLMService

from .models import Asset
from .serializers import AssetSerializer


class AssetViewSet(ModelViewSet):
    queryset = Asset.objects.select_related("airport")
    serializer_class = AssetSerializer

    @action(
        detail=True,
        methods=["post"],
        url_path="ask",
    )
    def ask(self, request, pk=None):
        asset = self.get_object()

        serializer = AssetQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data["question"]

        service = AssetLLMService()

        result = service.ask(
            asset=asset,
            question=question,
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )