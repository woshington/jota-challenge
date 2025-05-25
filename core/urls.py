from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core import views

router = DefaultRouter()
router.register(r'vertical', views.VerticalListView, basename='core-vertical')
router.register(r'plan', views.PlanListView, basename='core-plan')

urlpatterns = [
    # Include the router's URLs
    path('', include(router.urls)),
]
