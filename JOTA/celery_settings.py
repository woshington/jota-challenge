import os
from celery import Celery
from kombu import Exchange, Queue
from celery.schedules import crontab
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JOTA.settings')

# Cria a instância Celery
app = Celery('JOTA')

# Configura broker e backend
app.conf.broker_url = f'amqp://{config("RABBITMQ_USER", "guest")}:{config("RABBITMQ_PASSWORD", "guest")}@{config("RABBITMQ_HOST", "rabbitmq_jota")}:5672//'
app.conf.result_backend = 'rpc://'

# Configura timezone
app.conf.timezone = 'UTC'
app.conf.enable_utc = True

# Configura Exchange e Fila
app.conf.task_queues = (
    Queue(
        'periodic_tasks',
        Exchange('periodic_tasks', type='direct'),
        routing_key='periodic.#'
    ),
)

app.conf.task_routes = {
    'news.tasks.publish_news': {'queue': 'periodic_tasks'},
}

# Beat schedule para tarefa periódica
app.conf.beat_schedule = {
    'publish-news': {
        'task': 'news.tasks.publish_news',
        'schedule': crontab(minute='*', hour='*'),  # A cada minuto
        'options': {'queue': 'periodic_tasks'},
    },
}

# Descobre automaticamente as tasks nos apps Django
from django.conf import settings
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
