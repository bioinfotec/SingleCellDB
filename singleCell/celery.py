import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
# "sample_app" is name of the root app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'singleCell.settings')
app = Celery( 'singleCell',)
app.config_from_object("django.conf:settings", namespace="CELERY")
# Load task modules from all registered Django apps.
app.autodiscover_tasks()