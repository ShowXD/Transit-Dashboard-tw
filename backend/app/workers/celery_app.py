from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery_app = Celery(
    "parking_worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Taipei",
    enable_utc=True,
    beat_schedule={
        "sync-parking-master-data": {
            "task": "app.workers.tasks.sync_parking_master_data",
            "schedule": crontab(hour=3, minute=0),
        },
        "fetch-parking-availability": {
            "task": "app.workers.tasks.fetch_parking_availability",
            "schedule": 120.0,
        },
        "fetch-road-availability": {
            "task": "app.workers.tasks.fetch_road_availability",
            "schedule": 300.0,
        },
    },
    worker_concurrency=2,
    worker_pool="gevent",
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)
