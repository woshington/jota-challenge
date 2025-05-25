from django.utils import timezone
from celery import shared_task

@shared_task
def publish_news():
    from news.models import News
    News.objects.filter(
        status=News.Status.DRAFT,
        scheduled_at__lte=timezone.now()
    ).update(status=News.Status.PUBLISHED, published_at=timezone.now())