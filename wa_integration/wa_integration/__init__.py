"""
The project init file.
"""

from .celery import celery_app

__all__ = ('celery_app', )
