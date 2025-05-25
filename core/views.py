from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.custom_permissions import IsPublisherPermission, IsAdminPermission
from core.models import Vertical, Plan
from core.serializers import VerticalSerializer, PlanSerializer


# Create your views here.

class VerticalListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Vertical.objects.all()
    serializer_class = VerticalSerializer
    permission_classes = [IsAuthenticated]



class PlanListView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated]