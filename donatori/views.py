from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import mixins, permissions, viewsets, response

from .models import (
    Sesso,
    Sezione,
)
from .serializers import (
    SessoDetailSerializer,
    SessoSerializer,
    SezioneSerializer,
    UserSerializer,
)


class CurrentUserViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = User.objects.all().select_related('profiloutente', 'sezione')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        return response.Response(
            self.get_serializer(request.user).data
        )


class SezioneViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Sezione.objects.all()
    serializer_class = SezioneSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(utente=self.request.user)


class SessoViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Sesso.objects.all()
    serializer_class = SessoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return SessoSerializer
        return SessoDetailSerializer
