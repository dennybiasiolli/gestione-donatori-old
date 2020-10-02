from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CurrentUserViewSet,
    SezioneViewSet,
)


router = DefaultRouter()
router.register(r'me', CurrentUserViewSet)
router.register(r'sezioni', SezioneViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
