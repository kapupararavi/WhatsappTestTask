"""
Celery configuration for current project.
"""

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wa_integration.settings')
celery_app = Celery(__name__)

celery_app.config_from_object('django.conf.settings', namespace='CELERY')
celery_app.autodiscover_tasks()
