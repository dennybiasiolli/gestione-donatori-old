from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import mixins, permissions, viewsets, response

from .serializers import UserSerializer


class CurrentUserViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = User.objects.all().select_related('profiloutente', 'sezione')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        return response.Response(
            self.get_serializer(request.user).data
        )
