from django.contrib.auth.models import User
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions, renderers, viewsets, mixins

from .models import Sezione
from .serializers import SezioneSerializer, UserSerializer


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
        # if self.request.user.is_superuser:
        #     return Sezione.objects.all()
        return Sezione.objects.filter(owner=self.request.user)
