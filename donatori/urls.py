from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CurrentUserViewSet,
    DonatoreViewSet,
    SessoViewSet,
    SezioneViewSet,
    StatoDonatoreViewSet,
)


router = DefaultRouter()
router.register(r'me', CurrentUserViewSet)
router.register(r'sezioni', SezioneViewSet)
router.register(r'sessi', SessoViewSet)
router.register(r'stati-donatore', StatoDonatoreViewSet)
router.register(r'donatori', DonatoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
