"""
Contains the task(s) for the current app.
"""

import logging
from django.apps import apps
from celery import shared_task


@shared_task
def send_wa_message_task(pk: int):
    """
    Celery task to send the whatsapp message.

    Args:
        pk (int): Primary key value for the Whatsapp message
    """
    WhatsappMessage = apps.get_model('wa_messages.WhatsappMessage')  # pylint: disable=invalid-name
    try:
        wa_message_obj = WhatsappMessage.objects.get(pk=pk)
    except WhatsappMessage.DoesNotExist:
        logging.warning(f"No object with the primary key: {pk}")  # pylint: disable=logging-fstring-interpolation
        return

    wa_message_obj.send()
