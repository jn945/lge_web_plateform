from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig
from django.conf import settings


class MeasurementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.measurement"
