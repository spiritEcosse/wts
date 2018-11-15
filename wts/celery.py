from __future__ import absolute_import

from celery import Celery
from wts import settings

app = Celery(settings.PROJECT)
app.config_from_object('wts.settings', namespace='CELERY')
app.autodiscover_tasks(('wts', ), force=True)
