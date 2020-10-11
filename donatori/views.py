from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from rest_framework import mixins, permissions, viewsets, response

from .models import (
    Donatore,
    Donazione,
    Sesso,
    Sezione,
    StatoDonatore,
)
from .serializers import (
    DonatoreDetailSerializer,
    DonatoreListSerializer,
    DonatoreSerializer,
    DonazioneSerializer,
    SessoDetailSerializer,
    SessoSerializer,
    SezioneSerializer,
    StatoDonatoreSerializer,
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


class StatoDonatoreViewSet(viewsets.ModelViewSet):
    queryset = StatoDonatore.objects.all()
    serializer_class = StatoDonatoreSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            return self.queryset.filter(
                Q(utente__isnull=True) | Q(utente=self.request.user)
            )
        return self.queryset.filter(
            utente=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(utente=self.request.user)


class DonatoreViewSet(viewsets.ModelViewSet):
    queryset = Donatore.objects.all().select_related(
        'sezione', 'sesso', 'stato_donatore')
    serializer_class = DonatoreListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(
            sezione__utente=self.request.user
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return DonatoreListSerializer
        elif self.action == 'retrieve':
            return DonatoreDetailSerializer
        return DonatoreSerializer


class DonazioneViewSet(mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = Donazione.objects.all().select_related(
        'donatore', 'donatore__sezione')
    serializer_class = DonazioneSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(
            donatore__sezione__utente=self.request.user
        )
