from django.contrib.auth.models import User
from rest_framework import serializers

from .models import ProfiloUtente


class ProfiloUtenteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProfiloUtente
        fields = ('is_sezione', 'is_centro_di_raccolta', 'is_donatore',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profiloutente = ProfiloUtenteSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'profiloutente')
