"""
Contains models related to the messaging and API views, the API token model
class is added here, since there's no custom user model is defined and its
a demonstration.
"""

import hashlib
from requests.exceptions import HTTPError
from django.db import models
from django.conf import settings
from .utils import get_uuid4, get_random_letters
from .functions import send_wa_message
from .tasks import send_wa_message_task



class WhatsappUser(models.Model):
    wa_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, default='Unknown user')

    def __str__(self):
        return self.name


class Message(models.Model):
    """
    Stores message, any message send through the API must be added
    to this Model, and the `send` or `send_async` method should be
    used to send the message.
    """
    STATUS_PENDING = 'pending'
    STATUS_FAILED = 'failed'
    STATUS_SUCCESS = 'sent'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_SUCCESS, 'Sent')
    ]

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=24)
    content = models.TextField(max_length=4096)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_PENDING)
    api_response = models.JSONField(null=True, default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def send(self):
        """
        Method to send the message using current object information.
        """
        try:
            res = send_wa_message(self.receiver, self.content)
        except Exception as e:
            if isinstance(e, HTTPError):
                self.api_response = e.response.json()
            self.status = self.STATUS_FAILED
            raise e
        else:
            self.status = self.STATUS_SUCCESS
            self.api_response = res.json()
        finally:
            self.save()

    def send_async(self):
        """
        Uses the celery task to send the message in background.
        """
        send_wa_message_task.apply_async((self.pk, ))

    def __str__(self):
        return "Message"

    class Meta:
        abstract = True


class WhatsappMessage(Message):
    pass


class APIToken(models.Model):
    """
    API tokens for users, to identify the sender.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token_id = models.CharField(max_length=32, default=get_uuid4, unique=True)
    token = models.CharField(max_length=100, unique=True, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_token(cls, user):
        """
        Creates a new API token for the user object passed in
        the arguments.

        Returns:
            (str, `wa_messages.models.APIToken`) token string and the object of the token
        """
        random_text = get_random_letters(64)
        hashed_token = hashlib.sha256(random_text.encode()).hexdigest()
        return random_text, cls.objects.create(
            user=user,
            token=hashed_token
        )

    def __str__(self):
        return f"API token for {self.user}"


class TestWhatsappMessage(Message):
    status = models.CharField(max_length=32, choices=WhatsappMessage.STATUS_CHOICES, default=WhatsappMessage.STATUS_PENDING, editable=False)
    api_response = models.JSONField(null=True, default=None, blank=True, editable=False)

    def send_async(self):
        raise NotImplementedError


class ReceivedWhatsappMessage(models.Model):
    sender = models.ForeignKey(WhatsappUser, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=32, blank=True, default='text')
    content = models.TextField(max_length=4096, blank=True)
    sent_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender}"
