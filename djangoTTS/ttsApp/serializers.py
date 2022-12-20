from rest_framework import serializers


class TTSSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000)