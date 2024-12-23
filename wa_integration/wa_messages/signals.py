from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import TestWhatsappMessage


@receiver(post_save, sender=TestWhatsappMessage)
def send_test_whatsapp_message(instance: TestWhatsappMessage, created, **kwargs):
    if created:
        instance.send()
