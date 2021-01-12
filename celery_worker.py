"""configure celery worker instance."""

from config import AppConfig
from main import celery_app, create_app

app = create_app(AppConfig)
app.app_context().push()
