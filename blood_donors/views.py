from django.contrib.auth.models import User
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions, renderers, viewsets, mixins

from .models import (Sezione, CentroDiRaccolta, Sesso,
                     StatoDonatore, TipoDonazione, Donatore)
from .serializers import (SezioneSerializer, UserSerializer, CentroDiRaccoltaSerializer,
                          SessoSerializer, StatoDonatoreSerializer, TipoDonazioneSerializer,
                          DonatoreSerializer)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'sezioni': reverse('sezioni-list', request=request, format=format),
    })


class UsersViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SezioniViewSet(viewsets.ModelViewSet):
    queryset = Sezione.objects.all()
    serializer_class = SezioneSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Sezione.objects.filter(owner=self.request.user)


class CentriDiRaccoltaViewSet(viewsets.ModelViewSet):
    queryset = CentroDiRaccolta.objects.all()
    serializer_class = CentroDiRaccoltaSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # if self.request.user.is_superuser:
        #     return CentroDiRaccolta.objects.all()
        return CentroDiRaccolta.objects.filter(owner=self.request.user)


class SessiViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sesso.objects.all()
    serializer_class = SessoSerializer
    permission_classes = (permissions.IsAuthenticated,)


class StatiDonatoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StatoDonatore.objects.all()
    serializer_class = StatoDonatoreSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TipiDonazioneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoDonazione.objects.all()
    serializer_class = TipoDonazioneSerializer
    permission_classes = (permissions.IsAuthenticated,)


class DonatoriViewSet(viewsets.ModelViewSet):
    queryset = Donatore.objects.all()
    serializer_class = DonatoreSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # if self.request.user.is_superuser:
        #     return Donatore.objects.all()
        return Donatore.objects.filter(sezione__owner=self.request.user)
