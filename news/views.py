

from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.custom_permissions import IsPublisherPermission, IsAdminPermission
from news.models import News
from news.serializers import NewsSerializer


# Create your views here.

class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    """A viewset that provides default `create`, `retrieve`, and `update` actions."""
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsPublisherPermission | IsAdminPermission]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if not self.action in ['create', 'update', "partial_update", "publish_news"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        """
        Optionally restricts the returned news to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = super().get_queryset()
        user = self.request.user
        if user.role == user.READER:
            vertical_ids = []
            if not user.plan.is_basic:
                vertical_ids = list(user.plan.vertical.values_list('id', flat=True))
            return queryset.filter(
                status=News.Status.PUBLISHED
            ).filter(
                Q(is_open=True) | Q(vertical__id__in=vertical_ids),
            ).distinct()
        return queryset.distinct()

    @action(
        detail=True,
        methods=['post'],
        url_path='publish',
        permission_classes=[IsPublisherPermission | IsAdminPermission]
    )
    def publish_news(self, request, pk=None):
        """
        Custom action to publish a news item.
        """
        news = self.get_object()
        self.check_object_permissions(request, self.get_object())

        news.status = News.Status.PUBLISHED
        news.published_at = timezone.now()
        news.save()
        serializer = self.get_serializer(news)
        return Response(serializer.data)