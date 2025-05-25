from django.urls import path, include
from rest_framework.routers import DefaultRouter

from news import views

router = DefaultRouter()
router.register(r'', views.CreateListRetrieveViewSet, basename='news-publisher')

urlpatterns = [
    # Include the router's URLs
    path('', include(router.urls)),
]
