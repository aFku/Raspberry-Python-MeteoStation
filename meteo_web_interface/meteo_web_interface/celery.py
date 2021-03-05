import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meteo_web_interface.settings')

routine_measur = Celery('meteo_web_interface')

routine_measur.config_from_object('django.conf:settings', namespace='CELERY')

routine_measur.autodiscover_tasks()

