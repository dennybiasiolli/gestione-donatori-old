from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Sezione


class SezioneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sezione
        fields = ('descrizione',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    sezione = SezioneSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'sezione',)
