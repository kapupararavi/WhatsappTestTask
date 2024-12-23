"""
API views for the current app `wa_messages`
"""
import datetime
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import ReceivedWhatsappMessage, WhatsappUser

from wa_integration.authentication_classes import TokenAuth

from .serializers.request import SendMessageSerializer


class SendMessageAPIView(APIView):
    """
    API View to send the Whatsapp message.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuth]

    def post(self, request):        # pylint: disable=missing-function-docstring
        serializer = SendMessageSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        wa_message_obj = serializer.save()
        wa_message_obj.send_async()
        return Response({
            "status": "ok"
        }, status=status.HTTP_202_ACCEPTED)


class WAMessageWebhook(APIView):
    """
    APIView 
    """
    def get(self, request):
        return HttpResponse(request.GET['hub.challenge'], status=status.HTTP_200_OK)

    def post(self, request):
        object_name = request.data['object']
        if object_name == 'whatsapp_business_account':
            for entry in request.data['entry']:
                for change in entry['changes']:
                    if change['field'] == 'messages':
                        print(change)
                        user_name = change['value']['contacts'][0]['profile']['name']
                        from_message_id = change['value']['contacts'][0]['wa_id']
                        user, _ = WhatsappUser.objects.update_or_create(wa_id=from_message_id, defaults={
                            "name": user_name
                        })
                        for message in change['value']['messages']:
                            # handled text type only
                            kwargs = {
                                "sender": user,
                                "message_type": message['type'],
                                "content": '',
                                "sent_time": datetime.datetime.fromtimestamp(int(message['timestamp']))
                            }
                            if message['type'] == 'text':
                                kwargs['content'] = message['text']['body']
                            ReceivedWhatsappMessage.objects.create(**kwargs)
        return Response({
            "status": "ok"
        }, status=status.HTTP_200_OK)
