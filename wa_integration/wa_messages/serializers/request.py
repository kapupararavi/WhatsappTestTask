from rest_framework import serializers
from ..models import WhatsappMessage


class SendMessageSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=24,
        error_messages={}
    )
    message = serializers.CharField(
        max_length=4096,
        error_messages={}
    )

    def create(self, validated_data):
        user = self.context['user']
        return WhatsappMessage.objects.create(
            sender=user,
            receiver=validated_data['phone_number'],
            content=validated_data['message']
        )
