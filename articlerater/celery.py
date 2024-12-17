import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "articlerater.settings")

app = Celery("articlerater")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.result_expires = 180
app.conf.timezone = "UTC"


app.conf.beat_schedule = {
    "apply_rating_updates": {
        "task": "core.tasks.apply_rating_updates",
        'schedule': crontab(minute='*/1'),
    }
}
