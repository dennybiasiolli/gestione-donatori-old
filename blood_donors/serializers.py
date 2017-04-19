from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Sezione, CentroDiRaccolta, Sesso


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email',
                  'is_superuser', 'first_name', 'last_name')


class SezioneSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Sezione
        fields = ('__all__')


class CentroDiRaccoltaSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = CentroDiRaccolta
        fields = ('__all__')


class SessoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sesso
        fields = ('__all__')
