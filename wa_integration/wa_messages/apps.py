"""
`wa_messages` app configuration.
"""

from django.apps import AppConfig


class WaMessagesConfig(AppConfig):  # pylint: disable=missing-class-docstring
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wa_messages'

    def ready(self):
        from .import signals
