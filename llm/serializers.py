from rest_framework import serializers


class AssetQuestionSerializer(serializers.Serializer):
    question = serializers.CharField(
        max_length=1000,
        allow_blank=False,
    )