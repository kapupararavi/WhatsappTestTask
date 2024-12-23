"""
URL Patterns for the `wa_messages` app.
"""

from django.urls import path
from .views import SendMessageAPIView, WAMessageWebhook


urlpatterns = [
    path('v1/send', SendMessageAPIView.as_view(), name='send_wa_message_v1'),
    path('v1/webhook', WAMessageWebhook.as_view(), name='wa_webhook_v1')
]
