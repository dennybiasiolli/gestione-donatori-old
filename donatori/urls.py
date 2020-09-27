from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CurrentUserViewSet


router = DefaultRouter()
router.register(r'me', CurrentUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
