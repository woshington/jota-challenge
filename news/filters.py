import django_filters
from news.models import News

class NewsFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=News.Status.choices)
    is_open = django_filters.BooleanFilter()

    class Meta:
        model = News
        fields = ['status', 'is_open', 'vertical']
